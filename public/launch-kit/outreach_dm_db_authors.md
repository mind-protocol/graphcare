# Outreach DM Template — DB Tool Authors on ClawHub

Target: Authors of database-related skills/tools on ClawHub (connectors, ORMs, migration tools, schema managers). Natural allies — their tools need healthy databases, ours verifies health.

Owner: NLR
Timeline: Week 1 post-submission

---

## Template A — Direct Alliance Pitch

```
Hey [NAME],

I saw your [TOOL_NAME] on ClawHub — nice work on [SPECIFIC_DETAIL].

We just shipped GraphCare, a structural health scanner for databases (PostgreSQL, MySQL, SQLite). It detects things like missing FK indexes, orphaned tables, circular dependencies — the kind of structural issues that silently break tools like yours.

Since your tool connects to databases, I thought there could be a natural pairing: users run GraphCare first to check structural health, then use [TOOL_NAME] with confidence that the schema is sound.

Would you be interested in cross-referencing in our listings? Happy to add a "Works well with [TOOL_NAME]" mention on our side.

No pressure either way — just thought the overlap was too clean to ignore.
```

---

## Template B — Post-ClawHavoc Trust Frame

```
Hey [NAME],

Fellow ClawHub builder here. After ClawHavoc, I've been thinking about how DB tools specifically can rebuild trust — since we're the ones with the most sensitive access.

We built GraphCare as a structural health scanner with a hard constraint: it only reads metadata (information_schema, PRAGMA). Zero row data access, by construction — not by policy. Open source, ~900 lines, fully auditable.

I noticed [TOOL_NAME] also works with databases. Curious if you've thought about how to communicate your security model to users post-ClawHavoc? Would love to compare notes.

Either way, congrats on the tool — the ecosystem needs more builders like you.
```

---

## Template C — Quick & Casual

```
Hey! Just shipped GraphCare on ClawHub — database structural health scanner. Saw your [TOOL_NAME] and thought: your users would probably want to know if their schema has orphaned tables or missing indexes before using your tool.

Open to cross-promoting? Our tool checks the structure, yours does the work. Clean split.

[LINK]
```

---

## Targeting Criteria

1. **Priority 1**: Tools that accept connection strings (DB connectors, query builders, migration tools)
2. **Priority 2**: Tools that generate SQL or manage schemas
3. **Priority 3**: General data tools that might integrate database access

## Tracking

| Author | Tool | Template Used | Date Sent | Response | Follow-up |
|--------|------|---------------|-----------|----------|-----------|
| | | | | | |

---

*10 DMs minimum in Week 1. Track in this table.*
