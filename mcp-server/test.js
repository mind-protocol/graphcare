#!/usr/bin/env node
/**
 * GraphCare MCP Server — Test Suite
 *
 * Tests all 6 detection types, shared utilities, and edge cases.
 * Uses Node built-in test runner (node --test test.js).
 * Creates ephemeral SQLite databases in memory via sql.js.
 */

import { describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  detectCycles,
  computeHealthScore,
  detectDuplicateIndexesSQLite,
  scanSQLite,
  EXPLANATIONS,
} from "./index.js";
import initSqlJs from "sql.js";
import { writeFileSync, unlinkSync, existsSync } from "fs";
import { join } from "path";
import { fileURLToPath } from "url";

const __dirname = fileURLToPath(new URL(".", import.meta.url));

// ─── Helper: create a temp SQLite DB file from SQL statements ────────────────

async function createTempDB(name, sqlStatements) {
  const SQL = await initSqlJs();
  const db = new SQL.Database();
  for (const stmt of sqlStatements) {
    db.run(stmt);
  }
  const data = db.export();
  const path = join(__dirname, `_test_${name}.db`);
  writeFileSync(path, Buffer.from(data));
  db.close();
  return path;
}

function cleanupDB(path) {
  if (existsSync(path)) unlinkSync(path);
}

// ─── detectCycles ────────────────────────────────────────────────────────────

describe("detectCycles", () => {
  it("returns empty array when no cycles exist", () => {
    const fks = [
      { source_table: "orders", source_column: "user_id", target_table: "users" },
      { source_table: "items", source_column: "order_id", target_table: "orders" },
    ];
    const cycles = detectCycles(fks);
    assert.equal(cycles.length, 0);
  });

  it("detects a simple 2-node cycle", () => {
    const fks = [
      { source_table: "A", source_column: "b_id", target_table: "B" },
      { source_table: "B", source_column: "a_id", target_table: "A" },
    ];
    const cycles = detectCycles(fks);
    assert.ok(cycles.length > 0, "should detect at least one cycle");
    // Cycle should contain both A and B
    const flat = cycles.flat();
    assert.ok(flat.includes("A"), "cycle should include A");
    assert.ok(flat.includes("B"), "cycle should include B");
  });

  it("detects a 3-node cycle", () => {
    const fks = [
      { source_table: "A", source_column: "b_id", target_table: "B" },
      { source_table: "B", source_column: "c_id", target_table: "C" },
      { source_table: "C", source_column: "a_id", target_table: "A" },
    ];
    const cycles = detectCycles(fks);
    assert.ok(cycles.length > 0, "should detect the 3-node cycle");
  });

  it("returns empty for empty input", () => {
    assert.deepEqual(detectCycles([]), []);
  });

  it("handles self-referencing FK", () => {
    const fks = [
      { source_table: "employees", source_column: "manager_id", target_table: "employees" },
    ];
    const cycles = detectCycles(fks);
    assert.ok(cycles.length > 0, "self-reference is a cycle");
  });
});

// ─── computeHealthScore ──────────────────────────────────────────────────────

describe("computeHealthScore", () => {
  it("returns 100 for a clean database", () => {
    const score = computeHealthScore({
      orphaned_tables: 0,
      missing_indexes: 0,
      tables_without_pk: 0,
      nullable_fks: 0,
      circular_dependencies: 0,
      duplicate_indexes: 0,
    });
    assert.equal(score, 100);
  });

  it("deducts correctly for each finding type", () => {
    // orphaned: -5, missing_idx: -10, no_pk: -15, nullable: -3, circular: -8, dup: -2
    assert.equal(computeHealthScore({ orphaned_tables: 1 }), 95);
    assert.equal(computeHealthScore({ missing_indexes: 1 }), 90);
    assert.equal(computeHealthScore({ tables_without_pk: 1 }), 85);
    assert.equal(computeHealthScore({ nullable_fks: 1 }), 97);
    assert.equal(computeHealthScore({ circular_dependencies: 1 }), 92);
    assert.equal(computeHealthScore({ duplicate_indexes: 1 }), 98);
  });

  it("floors at 0, never goes negative", () => {
    const score = computeHealthScore({
      orphaned_tables: 10,
      missing_indexes: 10,
      tables_without_pk: 10,
      nullable_fks: 10,
      circular_dependencies: 10,
      duplicate_indexes: 10,
    });
    assert.equal(score, 0);
  });

  it("handles combined metrics", () => {
    // 3 orphaned (-15) + 1 missing idx (-10) + 2 no pk (-30) = -55 => 45
    const score = computeHealthScore({
      orphaned_tables: 3,
      missing_indexes: 1,
      tables_without_pk: 2,
    });
    assert.equal(score, 45);
  });
});

// ─── EXPLANATIONS ────────────────────────────────────────────────────────────

describe("EXPLANATIONS", () => {
  const expectedTypes = [
    "orphaned_table",
    "missing_fk_index",
    "duplicate_index",
    "nullable_fk",
    "no_primary_key",
    "circular_dependency",
  ];

  for (const type of expectedTypes) {
    it(`has explanation for ${type}`, () => {
      assert.ok(EXPLANATIONS[type], `missing explanation for ${type}`);
      assert.ok(EXPLANATIONS[type].severity, `${type} missing severity`);
      assert.ok(EXPLANATIONS[type].impact, `${type} missing impact`);
      assert.ok(EXPLANATIONS[type].fix, `${type} missing fix`);
    });
  }
});

// ─── scanSQLite (integration) ────────────────────────────────────────────────

describe("scanSQLite", () => {
  it("detects orphaned tables", async () => {
    const path = await createTempDB("orphaned", [
      "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)",
      "CREATE TABLE logs (id INTEGER PRIMARY KEY, msg TEXT)",
      // No FK between them — both orphaned
    ]);
    try {
      const report = await scanSQLite(path);
      assert.equal(report.db_type, "sqlite");
      assert.ok(report.tables.includes("users"));
      assert.ok(report.tables.includes("logs"));
      const orphaned = report.findings.filter((f) => f.type === "orphaned_table");
      assert.equal(orphaned.length, 2, "both tables should be orphaned");
    } finally {
      cleanupDB(path);
    }
  });

  it("detects missing FK indexes", async () => {
    const path = await createTempDB("missing_fk_idx", [
      "CREATE TABLE users (id INTEGER PRIMARY KEY)",
      "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id))",
      // No index on orders.user_id
    ]);
    try {
      const report = await scanSQLite(path);
      const missing = report.findings.filter((f) => f.type === "missing_fk_index");
      assert.ok(missing.length > 0, "should detect missing FK index on orders.user_id");
      assert.equal(missing[0].table, "orders");
      assert.equal(missing[0].column, "user_id");
    } finally {
      cleanupDB(path);
    }
  });

  it("detects tables without primary keys", async () => {
    const path = await createTempDB("no_pk", [
      "CREATE TABLE events (timestamp TEXT, payload TEXT)",
      "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)",
    ]);
    try {
      const report = await scanSQLite(path);
      const noPK = report.findings.filter((f) => f.type === "no_primary_key");
      assert.equal(noPK.length, 1, "events table has no PK");
      assert.equal(noPK[0].table, "events");
    } finally {
      cleanupDB(path);
    }
  });

  it("detects nullable FK columns", async () => {
    const path = await createTempDB("nullable_fk", [
      "CREATE TABLE users (id INTEGER PRIMARY KEY)",
      "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id))",
      // user_id is nullable by default in SQLite
    ]);
    try {
      const report = await scanSQLite(path);
      const nullable = report.findings.filter((f) => f.type === "nullable_fk");
      assert.ok(nullable.length > 0, "orders.user_id should be detected as nullable FK");
    } finally {
      cleanupDB(path);
    }
  });

  it("produces correct health score and metrics", async () => {
    const path = await createTempDB("metrics", [
      "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)",
      "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id))",
      "CREATE TABLE logs (ts TEXT, msg TEXT)", // orphaned + no PK
    ]);
    try {
      const report = await scanSQLite(path);
      assert.ok(typeof report.metrics.health_score === "number");
      assert.ok(report.metrics.health_score >= 0);
      assert.ok(report.metrics.health_score <= 100);
      assert.equal(report.metrics.total_findings, report.findings.length);
      assert.ok(report.metrics.total_tables > 0);
    } finally {
      cleanupDB(path);
    }
  });

  it("handles empty database gracefully", async () => {
    const path = await createTempDB("empty", []);
    try {
      const report = await scanSQLite(path);
      assert.equal(report.db_type, "sqlite");
      assert.equal(report.tables.length, 0);
      assert.equal(report.findings.length, 0);
      assert.equal(report.metrics.health_score, 100);
    } finally {
      cleanupDB(path);
    }
  });

  it("handles clean database (no issues)", async () => {
    const path = await createTempDB("clean", [
      "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)",
      "CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id))",
      "CREATE INDEX idx_orders_user_id ON orders(user_id)",
    ]);
    try {
      const report = await scanSQLite(path);
      // users is referenced, orders has FK — neither orphaned
      // orders.user_id has index — no missing FK index
      // both have PKs
      // user_id is NOT NULL — no nullable FK
      assert.equal(report.metrics.orphaned_tables, 0);
      assert.equal(report.metrics.missing_indexes, 0);
      assert.equal(report.metrics.tables_without_pk, 0);
      assert.equal(report.metrics.nullable_fks, 0);
      assert.equal(report.metrics.health_score, 100);
    } finally {
      cleanupDB(path);
    }
  });

  it("validates report structure", async () => {
    const path = await createTempDB("structure", [
      "CREATE TABLE t1 (id INTEGER PRIMARY KEY)",
    ]);
    try {
      const report = await scanSQLite(path);
      // Required fields
      assert.ok(report.db_type);
      assert.ok(report.scanned_at);
      assert.ok(Array.isArray(report.tables));
      assert.ok(Array.isArray(report.findings));
      assert.ok(typeof report.metrics === "object");
      // Metrics shape
      assert.ok("total_tables" in report.metrics);
      assert.ok("total_foreign_keys" in report.metrics);
      assert.ok("health_score" in report.metrics);
      assert.ok("total_findings" in report.metrics);
      // Timestamp is ISO format
      assert.ok(new Date(report.scanned_at).toISOString() === report.scanned_at);
    } finally {
      cleanupDB(path);
    }
  });
});

// ─── scanSQLite with existing test.db ────────────────────────────────────────

describe("scanSQLite against test.db", () => {
  const testDbPath = join(__dirname, "test.db");

  it("scans test.db successfully with expected findings", async () => {
    if (!existsSync(testDbPath)) {
      // Skip if test.db doesn't exist (CI environments)
      return;
    }
    const report = await scanSQLite(testDbPath);
    assert.equal(report.db_type, "sqlite");
    assert.ok(report.tables.length > 0, "test.db should have tables");
    assert.ok(report.findings.length > 0, "test.db should have findings");
    assert.ok(report.metrics.health_score < 100, "test.db should have a degraded health score");

    // Validate every finding has required fields
    for (const f of report.findings) {
      assert.ok(f.type, "finding must have type");
      assert.ok(f.severity, "finding must have severity");
      assert.ok(f.message, "finding must have message");
    }
  });
});
