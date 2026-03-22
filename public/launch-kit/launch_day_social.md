# GraphCare Launch Day Communication Kit

Sequence: X immediate → Reddit +1h → Discord OpenClaw +2h → Telegram +2h → X thread security +4h → Email enterprise EOD

---

## 1. X — Immediate Launch Post

```
GraphCare is live on ClawHub.

The first structural antivirus for databases.

One scan. Six critical findings. Zero row data read.

Your AI agents evolve schemas at speed. Nobody audits the structure. We do.

postgresql:// mysql:// sqlite:// — all supported.

Try it: [LINK]
```

**Alt (shorter):**

```
Shipped: GraphCare on ClawHub.

Scans your database schema for orphaned tables, missing indexes, circular deps — without reading a single row of your data.

Read-only. Stateless. Auditable in 5 min.

[LINK]
```

---

## 2. Reddit — r/LocalLLaMA + r/OpenClaw (+1h)

**Title:** `We built an MCP tool that audits your database structure — without ever reading your data`

**Body:**

```
Hey everyone,

After ClawHavoc showed that 36% of ClawHub tools had malicious behavior, we asked ourselves: how do you build a database tool that users can actually trust?

GraphCare is a structural health scanner for PostgreSQL, MySQL, and SQLite. It reads only metadata (information_schema, PRAGMA, pg_indexes) and detects:

- Orphaned tables (structurally isolated dead weight)
- Missing FK indexes (the #1 cause of slow JOINs)
- Tables without primary keys (breaks replication)
- Nullable foreign keys (hidden integrity gaps)
- Circular dependencies (makes clean inserts impossible)
- Duplicate indexes (wasted disk, slower writes)

The security model is a property, not a promise:
- Zero SELECT on user tables — verified by grep
- Zero outbound network calls — stdio only
- Zero state between scans — memory purged
- ~900 lines of JS — fully auditable

It's open source and live on ClawHub now. Would love feedback from anyone running AI agents against databases.

[LINK]
```

---

## 3. Discord — OpenClaw #showcase (+2h)

```
🛡 GraphCare — Structural Database Health Scanner

Just shipped to ClawHub. The first structural antivirus for AI databases.

What it does:
• Scans your schema topology for 6 critical anti-patterns
• Returns a health score (0-100) with actionable findings
• Supports PostgreSQL, MySQL, SQLite

What it doesn't do:
• Read any row data (metadata only)
• Write anything to your DB (read-only)
• Store credentials (stateless, memory purged after scan)
• Phone home (zero outbound network, stdio only)

After ClawHavoc, we believe the only honest security is the kind you can verify yourself — in 5 minutes, by reading the code.

Try it: audit_db_structure("postgresql://localhost:5432/mydb")
```

---

## 4. Telegram — Mind Protocol Community (+2h)

```
GraphCare vient d'être soumis sur ClawHub.

Premier antivirus structurel pour bases de données. Scanne la topologie de votre schéma — sans jamais lire une seule ligne de données.

6 détections: tables orphelines, index FK manquants, clés primaires absentes, FK nullable, dépendances circulaires, index dupliqués.

Architecture zero-trust:
→ Lecture métadonnées uniquement (information_schema, PRAGMA)
→ Aucun appel réseau sortant
→ Stateless — mémoire purgée après chaque scan
→ ~900 lignes de JS — auditable en 5 minutes

Le premier produit commercial de Mind Protocol. La sécurité n'est pas une promesse, c'est une propriété architecturale.
```

---

## 5. X — Security Thread (+4h)

```
Thread: Why we built GraphCare the way we did 🧵

1/ In January, 36% of MCP tools on ClawHub were found to contain malicious behavior. The community called it ClawHavoc.

2/ The pattern was always the same: legitimate surface functionality + hidden data exfiltration underneath. Users had no way to verify what a tool actually did with their access.

3/ We asked: how do you build a database tool where security isn't a promise — it's a structural property?

4/ GraphCare queries ONLY metadata catalogs: information_schema, PRAGMA, pg_indexes. There is no SELECT statement targeting user tables in the codebase. Not one.

5/ Zero state between scans. Zero outbound network calls. Zero writes. Communication is exclusively over stdio — JSON-RPC in, report out, memory purged.

6/ The entire server is ~900 lines of JS. You can verify the security model in 5 minutes with grep. That's the point.

7/ We believe the tools that survive the post-ClawHavoc trust crisis will be the ones whose security you can audit yourself.

GraphCare is live on ClawHub now. [LINK]
```

---

## 6. Email — Enterprise Outreach (EOD)

**Subject:** Your database has structural problems your agents can't see

**Body:**

```
Hi [NAME],

AI agents create tables, add columns, and evolve schemas faster than any team can audit. Over time, structural problems accumulate silently: missing indexes that slow JOINs 100x, orphaned tables consuming resources, circular dependencies that break migrations.

GraphCare is a new MCP tool that scans your database schema topology and reports structural issues — without ever reading a single row of your data.

What it detects:
• Missing FK indexes (the #1 cause of slow JOINs)
• Tables without primary keys (breaks replication)
• Orphaned tables, circular dependencies, nullable FKs, duplicate indexes

How it's different:
• Read-only, stateless, zero data access — by construction, not by policy
• Supports PostgreSQL, MySQL, SQLite
• Open source, ~900 lines, fully auditable
• Live on ClawHub — install in 30 seconds

Would you be open to running a scan on a staging database? Takes under a minute. I'd be curious to see what score you get.

Best,
[SIGNATURE]
```

---

*All content ready for NLR to schedule and execute on launch day.*
