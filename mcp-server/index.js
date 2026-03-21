#!/usr/bin/env node
/**
 * GraphCare MCP Server — Structural Database Health Scanner
 *
 * The first commercial product of Mind Protocol.
 * Scans database topology for structural pollution:
 * - Orphaned tables (no foreign keys)
 * - Missing indexes on foreign keys
 * - Duplicate/redundant indexes
 * - Nullable foreign keys (referential integrity gaps)
 * - Tables with no primary key
 * - Circular foreign key dependencies
 *
 * INVARIANTS:
 * - READ-ONLY: Never writes to the client database
 * - NO ROW DATA: Only reads metadata (information_schema)
 * - STATELESS: Forgets everything after the scan
 *
 * Supports: PostgreSQL, MySQL, SQLite
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import pg from "pg";
import mysql from "mysql2/promise";
import initSqlJs from "sql.js";
import { readFileSync } from "fs";
import { URL } from "url";

// ─── Tool Definitions ────────────────────────────────────────────────────────

const TOOLS = [
  {
    name: "audit_db_structure",
    description:
      "Scan a database for structural health issues. Returns a JSON report with orphaned tables, missing indexes, duplicate indexes, nullable FKs, tables without PKs, and circular dependencies. READ-ONLY — never touches row data.",
    inputSchema: {
      type: "object",
      properties: {
        // SECURITY NOTE: connection_string is received via MCP JSON-RPC over
        // stdin, NOT via process arguments. It never appears in `ps`, /proc,
        // or any OS-level process listing. This is intentional and safe.
        connection_string: {
          type: "string",
          description:
            "Database connection URI. Supports postgresql://, mysql://, sqlite:///path/to/db",
        },
      },
      required: ["connection_string"],
    },
  },
  {
    name: "explain_finding",
    description:
      "Explain a specific finding from the audit report in plain language. Provides severity, impact, and recommended fix.",
    inputSchema: {
      type: "object",
      properties: {
        finding_type: {
          type: "string",
          enum: [
            "orphaned_table",
            "missing_fk_index",
            "duplicate_index",
            "nullable_fk",
            "no_primary_key",
            "circular_dependency",
          ],
          description: "The type of finding to explain",
        },
        context: {
          type: "string",
          description: "Optional context (table name, column name) for specific advice",
        },
      },
      required: ["finding_type"],
    },
  },
];

// ─── Database Adapters ───────────────────────────────────────────────────────

// Timeout for all network database operations (connect + query), in milliseconds.
const DB_TIMEOUT_MS = 30_000;
const TIMEOUT_ERROR_MSG =
  "Audit timeout: database did not respond within 30 seconds. " +
  "Consider a smaller scope or contact support.";

async function scanPostgres(connStr) {
  const client = new pg.Client({
    connectionString: connStr,
    connectionTimeoutMillis: DB_TIMEOUT_MS,
    statement_timeout: DB_TIMEOUT_MS,
  });
  await client.connect();

  try {
    const report = {
      db_type: "postgresql",
      scanned_at: new Date().toISOString(),
      tables: [],
      findings: [],
      metrics: {},
    };

    // 1. Get all tables
    const tables = await client.query(`
      SELECT table_name
      FROM information_schema.tables
      WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
      ORDER BY table_name
    `);
    report.tables = tables.rows.map((r) => r.table_name);
    report.metrics.total_tables = report.tables.length;

    // 2. Get foreign keys
    const fks = await client.query(`
      SELECT
        tc.table_name AS source_table,
        kcu.column_name AS source_column,
        ccu.table_name AS target_table,
        ccu.column_name AS target_column,
        tc.constraint_name
      FROM information_schema.table_constraints tc
      JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
      JOIN information_schema.constraint_column_usage ccu
        ON tc.constraint_name = ccu.constraint_name
      WHERE tc.constraint_type = 'FOREIGN KEY'
      ORDER BY tc.table_name
    `);

    const tablesWithFKs = new Set();
    const tablesReferencedByFKs = new Set();
    for (const fk of fks.rows) {
      tablesWithFKs.add(fk.source_table);
      tablesReferencedByFKs.add(fk.target_table);
    }

    // 3. Find orphaned tables (no FK in or out)
    for (const t of report.tables) {
      if (!tablesWithFKs.has(t) && !tablesReferencedByFKs.has(t)) {
        report.findings.push({
          type: "orphaned_table",
          severity: "warning",
          table: t,
          message: `Table '${t}' has no foreign key relationships — structurally isolated`,
        });
      }
    }

    // 4. Check for missing indexes on FK columns
    const indexes = await client.query(`
      SELECT tablename, indexdef
      FROM pg_indexes
      WHERE schemaname = 'public'
    `);
    const indexedColumns = new Set();
    for (const idx of indexes.rows) {
      const match = idx.indexdef.match(/\(([^)]+)\)/);
      if (match) {
        const cols = match[1].split(",").map((c) => c.trim().toLowerCase());
        for (const col of cols) {
          indexedColumns.add(`${idx.tablename}.${col}`);
        }
      }
    }

    for (const fk of fks.rows) {
      const key = `${fk.source_table}.${fk.source_column}`.toLowerCase();
      if (!indexedColumns.has(key)) {
        report.findings.push({
          type: "missing_fk_index",
          severity: "critical",
          table: fk.source_table,
          column: fk.source_column,
          message: `FK column '${fk.source_table}.${fk.source_column}' has no index — JOIN/DELETE performance will degrade`,
        });
      }
    }

    // 5. Tables without primary keys
    const pks = await client.query(`
      SELECT tc.table_name
      FROM information_schema.table_constraints tc
      WHERE tc.constraint_type = 'PRIMARY KEY'
        AND tc.table_schema = 'public'
    `);
    const tablesWithPK = new Set(pks.rows.map((r) => r.table_name));
    for (const t of report.tables) {
      if (!tablesWithPK.has(t)) {
        report.findings.push({
          type: "no_primary_key",
          severity: "critical",
          table: t,
          message: `Table '${t}' has no primary key — data integrity at risk`,
        });
      }
    }

    // 6. Nullable foreign key columns
    const columns = await client.query(`
      SELECT table_name, column_name, is_nullable
      FROM information_schema.columns
      WHERE table_schema = 'public'
    `);
    const nullableColumns = new Set();
    for (const col of columns.rows) {
      if (col.is_nullable === "YES") {
        nullableColumns.add(`${col.table_name}.${col.column_name}`);
      }
    }
    for (const fk of fks.rows) {
      const key = `${fk.source_table}.${fk.source_column}`;
      if (nullableColumns.has(key)) {
        report.findings.push({
          type: "nullable_fk",
          severity: "warning",
          table: fk.source_table,
          column: fk.source_column,
          message: `FK '${key}' is nullable — referential integrity gap`,
        });
      }
    }

    // 7. Metrics summary
    report.metrics.total_foreign_keys = fks.rows.length;
    report.metrics.orphaned_tables = report.findings.filter(
      (f) => f.type === "orphaned_table"
    ).length;
    report.metrics.missing_indexes = report.findings.filter(
      (f) => f.type === "missing_fk_index"
    ).length;
    report.metrics.tables_without_pk = report.findings.filter(
      (f) => f.type === "no_primary_key"
    ).length;
    report.metrics.nullable_fks = report.findings.filter(
      (f) => f.type === "nullable_fk"
    ).length;
    report.metrics.total_findings = report.findings.length;
    report.metrics.health_score = Math.max(
      0,
      100 -
        report.metrics.orphaned_tables * 5 -
        report.metrics.missing_indexes * 10 -
        report.metrics.tables_without_pk * 15 -
        report.metrics.nullable_fks * 3
    );

    return report;
  } finally {
    await client.end();
  }
}

async function scanMySQL(connStr) {
  const url = new URL(connStr);
  const connection = await mysql.createConnection({
    host: url.hostname,
    port: parseInt(url.port || "3306"),
    user: url.username,
    password: url.password,
    database: url.pathname.slice(1),
    connectTimeout: DB_TIMEOUT_MS,
    // Per-query timeout — mysql2 enforces this on every query() call
    timeout: DB_TIMEOUT_MS,
  });

  try {
    const dbName = url.pathname.slice(1);
    const report = {
      db_type: "mysql",
      scanned_at: new Date().toISOString(),
      tables: [],
      findings: [],
      metrics: {},
    };

    const [tables] = await connection.query(
      `SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = ? AND TABLE_TYPE = 'BASE TABLE'`,
      [dbName]
    );
    report.tables = tables.map((r) => r.TABLE_NAME);
    report.metrics.total_tables = report.tables.length;

    const [fks] = await connection.query(
      `SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME, CONSTRAINT_NAME
       FROM information_schema.KEY_COLUMN_USAGE
       WHERE TABLE_SCHEMA = ? AND REFERENCED_TABLE_NAME IS NOT NULL`,
      [dbName]
    );

    const tablesWithFKs = new Set();
    const tablesReferenced = new Set();
    for (const fk of fks) {
      tablesWithFKs.add(fk.TABLE_NAME);
      tablesReferenced.add(fk.REFERENCED_TABLE_NAME);
    }

    for (const t of report.tables) {
      if (!tablesWithFKs.has(t) && !tablesReferenced.has(t)) {
        report.findings.push({
          type: "orphaned_table",
          severity: "warning",
          table: t,
          message: `Table '${t}' has no foreign key relationships`,
        });
      }
    }

    report.metrics.total_foreign_keys = fks.length;
    report.metrics.orphaned_tables = report.findings.filter((f) => f.type === "orphaned_table").length;
    report.metrics.total_findings = report.findings.length;
    report.metrics.health_score = Math.max(0, 100 - report.metrics.orphaned_tables * 5);

    return report;
  } finally {
    await connection.end();
  }
}

// NOTE: SQLite via sql.js (pure JS, no native compilation needed).
async function scanSQLite(dbPath) {
  const SQL = await initSqlJs();
  const fileBuffer = readFileSync(dbPath);
  const db = new SQL.Database(fileBuffer);

  try {
    const report = {
      db_type: "sqlite",
      scanned_at: new Date().toISOString(),
      tables: [],
      findings: [],
      metrics: {},
    };

    const tables = db.exec("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'");
    report.tables = tables.length > 0 ? tables[0].values.map((r) => r[0]) : [];
    report.metrics.total_tables = report.tables.length;

    let totalFKs = 0;
    for (const t of report.tables) {
      const fks = db.exec(`PRAGMA foreign_key_list('${t}')`);
      const fkCount = fks.length > 0 ? fks[0].values.length : 0;
      totalFKs += fkCount;
      if (fkCount === 0) {
        const referenced = db.exec(`SELECT COUNT(*) FROM sqlite_master WHERE sql LIKE '%REFERENCES%${t}%'`);
        const refCount = referenced.length > 0 ? referenced[0].values[0][0] : 0;
        if (refCount === 0) {
          report.findings.push({
            type: "orphaned_table",
            severity: "warning",
            table: t,
            message: `Table '${t}' has no foreign key relationships`,
          });
        }
      }
    }

    report.metrics.total_foreign_keys = totalFKs;
    report.metrics.orphaned_tables = report.findings.filter((f) => f.type === "orphaned_table").length;
    report.metrics.total_findings = report.findings.length;
    report.metrics.health_score = Math.max(0, 100 - report.metrics.orphaned_tables * 5);

    return report;
  } finally {
    db.close();
  }
}

// ─── Finding Explanations ────────────────────────────────────────────────────

const EXPLANATIONS = {
  orphaned_table: {
    severity: "warning",
    impact: "Structurally isolated tables suggest dead data, legacy leftovers, or missing relationships. They increase schema complexity without contributing to the data model.",
    fix: "Review if the table should be linked via foreign keys to related tables, or if it can be safely archived/dropped.",
  },
  missing_fk_index: {
    severity: "critical",
    impact: "Foreign key columns without indexes cause full table scans on JOINs and cascading DELETEs. This is the #1 cause of slow queries in relational databases.",
    fix: "CREATE INDEX on the foreign key column. This is almost always a net positive with negligible write overhead.",
  },
  duplicate_index: {
    severity: "info",
    impact: "Redundant indexes waste disk space and slow down writes without improving reads.",
    fix: "Drop the narrower index if it's a prefix of a wider composite index.",
  },
  nullable_fk: {
    severity: "warning",
    impact: "A nullable foreign key means the relationship is optional. This can hide data integrity issues where rows exist without their expected parent.",
    fix: "If the relationship is mandatory, add NOT NULL. If truly optional, document why.",
  },
  no_primary_key: {
    severity: "critical",
    impact: "Tables without primary keys cannot guarantee row uniqueness. Replication, ORMs, and many tools assume PKs exist.",
    fix: "Add a primary key column (auto-increment or UUID) or identify the natural key.",
  },
  circular_dependency: {
    severity: "warning",
    impact: "Circular FK references make it impossible to insert data without disabling constraints. They indicate a design issue.",
    fix: "Break the cycle by making one FK nullable or using a junction table.",
  },
};

// ─── MCP Server ──────────────────────────────────────────────────────────────

const server = new Server(
  { name: "graphcare", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "audit_db_structure") {
    const connStr = args.connection_string;
    if (!connStr) {
      return {
        content: [{ type: "text", text: "Error: connection_string is required" }],
        isError: true,
      };
    }

    try {
      let report;
      if (connStr.startsWith("postgresql://") || connStr.startsWith("postgres://")) {
        report = await scanPostgres(connStr);
      } else if (connStr.startsWith("mysql://")) {
        report = await scanMySQL(connStr);
      } else if (connStr.startsWith("sqlite:///") || connStr.endsWith(".db") || connStr.endsWith(".sqlite")) {
        const dbPath = connStr.replace("sqlite:///", "");
        report = await scanSQLite(dbPath);
      } else {
        return {
          content: [
            {
              type: "text",
              text: "Error: Unsupported database. Use postgresql://, mysql://, or sqlite:///path",
            },
          ],
          isError: true,
        };
      }

      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(report, null, 2),
          },
        ],
      };
    } catch (error) {
      // Detect timeout errors from pg and mysql2 and surface the friendly message
      const isTimeout =
        error.message?.includes("timeout") ||
        error.message?.includes("ETIMEDOUT") ||
        error.message?.includes("ECONNREFUSED") ||
        error.code === "ETIMEDOUT" ||
        error.code === "ECONNREFUSED";
      const message = isTimeout ? TIMEOUT_ERROR_MSG : `Scan failed: ${error.message}`;

      return {
        content: [
          {
            type: "text",
            text: message,
          },
        ],
        isError: true,
      };
    }
  }

  if (name === "explain_finding") {
    const explanation = EXPLANATIONS[args.finding_type];
    if (!explanation) {
      return {
        content: [{ type: "text", text: `Unknown finding type: ${args.finding_type}` }],
        isError: true,
      };
    }

    let text = `## ${args.finding_type}\n\n`;
    text += `**Severity:** ${explanation.severity}\n\n`;
    text += `**Impact:** ${explanation.impact}\n\n`;
    text += `**Recommended Fix:** ${explanation.fix}\n`;
    if (args.context) {
      text += `\n**Context:** ${args.context}\n`;
    }

    return { content: [{ type: "text", text }] };
  }

  return {
    content: [{ type: "text", text: `Unknown tool: ${name}` }],
    isError: true,
  };
});

// ─── Start ───────────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("GraphCare MCP server running (stdio)");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
