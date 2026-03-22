# GraphCare

**Structural database health scanner — the first antivirus for your schema.**

GraphCare is an MCP server that audits your database topology for silent structural problems — orphaned tables, missing indexes, nullable foreign keys, circular dependencies — **without ever reading a single row of your data**.

## Why

AI agents evolve schemas at speed. Nobody audits the structure. Over time:

- Foreign keys lose their indexes — JOINs slow to a crawl
- Tables drift into isolation — orphaned, unreachable data
- Primary keys go missing — replication breaks, ORMs fail
- Nullable FKs create silent referential gaps
- Circular dependencies make inserts impossible
- Redundant indexes waste disk and slow writes

One scan catches all of it.

## Zero-Trust Design

GraphCare queries **only metadata** (`information_schema`, `PRAGMA`, `pg_indexes`). It is structurally impossible for it to read, leak, or mutate your row data.

| Guarantee | How |
|-----------|-----|
| **Read-only** | Zero writes, zero mutations |
| **No row data** | Only schema metadata accessed |
| **Stateless** | Memory purged after every scan |
| **No credential storage** | Connection string via MCP stdin, never in process listings |

## Quick Start

### Via npx (recommended)

```bash
npx graphcare-mcp
```

### Manual install

```bash
npm install -g graphcare-mcp
graphcare-mcp
```

### Docker

```bash
docker build -t graphcare .
docker run -i graphcare
```

### MCP Client Config

```json
{
  "mcpServers": {
    "graphcare": {
      "command": "npx",
      "args": ["-y", "graphcare-mcp"]
    }
  }
}
```

## Tools

### `audit_db_structure`

Full structural scan. Returns a complete health report.

**Input:** `connection_string` — Database URI (`postgresql://`, `mysql://`, `sqlite:///path/to/db`)

**Output:** JSON report with:
- `db_type` — Detected database engine
- `tables[]` — All tables found
- `findings[]` — Each issue with type, severity, table, message
- `metrics{}` — Counts per finding type + `health_score` (0–100)

### `explain_finding`

Plain-language explanation of any finding type with severity, impact, and recommended fix.

**Input:** `finding_type` — One of: `orphaned_table`, `missing_fk_index`, `duplicate_index`, `nullable_fk`, `no_primary_key`, `circular_dependency`

**Optional:** `context` — Table or column name for specific advice

## Detection Suite

| Finding | Severity | Impact |
|---------|----------|--------|
| Orphaned Tables | Warning | Structurally isolated dead weight |
| Missing FK Indexes | **Critical** | #1 cause of slow JOINs and cascading DELETEs |
| No Primary Key | **Critical** | Breaks replication, ORMs, and row identity |
| Nullable Foreign Keys | Warning | Hidden referential integrity gaps |
| Circular Dependencies | Warning | Clean inserts become impossible |
| Duplicate Indexes | Info | Wasted disk space, slower writes |

## Supported Databases

- **PostgreSQL** — Full 6-finding detection via `information_schema` + `pg_indexes`
- **MySQL** — Full 6-finding detection via `information_schema`
- **SQLite** — Full 6-finding detection via `sqlite_master` + `PRAGMA`

## Security

This tool runs read-only queries against database metadata catalogs only. It never executes `SELECT` on user tables, never writes, and holds no state between invocations. Connection strings are received via MCP JSON-RPC over stdin — never exposed in process listings.

## License

MIT

---

Built by [Mind Protocol](https://mindprotocol.ai).
