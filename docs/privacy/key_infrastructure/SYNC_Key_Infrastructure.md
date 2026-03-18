# Key Infrastructure — Sync: Current State

```
LAST_UPDATED: 2026-03-15
UPDATED_BY: @vox (doc chain creation)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The dual encryption model: GraphCare key for topology, citizen key for content
- Public key distribution via `mind init`
- Opt-out via key removal
- Key rotation as a periodic process

**What's still being designed:**
- Exact key format and cryptographic algorithm (RSA vs Ed25519 vs other)
- Key storage infrastructure for GraphCare's private key
- Key rotation cadence and transition period duration
- Monitoring for distinguishing opt-out from infrastructure failure

**What's proposed (v2+):**
- Key health dashboard showing distribution status across all citizens
- GraphCare public key published in L4 registry for independent verification
- Forward secrecy improvements (per-session keys derived from the master pair)

---

## CURRENT STATE

The key infrastructure exists only as design documentation. No code has been written. The topology-only principle it enforces is currently maintained through code discipline and test coverage — every scoring formula uses only the 7 primitives, and the test suite checks for content references in intervention messages.

The design is informed by the ALGORITHM doc for Daily Citizen Health, which describes the flow: "Fetch brain topology via brain_url, decrypt with GraphCare private key." The PATTERNS doc for Daily Citizen Health describes the two-layer model: "The brain graph is local to the citizen, but GraphCare holds a key that decrypts only the topology."

The gap: this is all described in prose but not implemented in code. Building the key infrastructure is the step that turns the topology-only principle from a convention into a guarantee.

---

## IN PROGRESS

### Doc chain creation
- **Started:** 2026-03-15
- **By:** @vox
- **Status:** Complete
- **Context:** First formalization of the key infrastructure as its own module. The dual encryption model was previously described only in the Daily Citizen Health ALGORITHM and PATTERNS docs. Now has its own chain focused on the cryptographic mechanisms.

---

## RECENT CHANGES

### 2026-03-15: Doc chain created

- **What:** Created full doc chain (OBJECTIVES, PATTERNS, VALIDATION, SYNC)
- **Why:** The key infrastructure is the enforcement mechanism for GraphCare's most important principle. It deserves dedicated documentation, not a subsection of the daily health check.
- **Files:** `docs/privacy/key_infrastructure/` (4 files)
- **Insights:** Several open questions surfaced during documentation — algorithm selection, storage infrastructure, rotation cadence. These are properly escalated in markers.

---

## KNOWN ISSUES

### No implementation exists

- **Severity:** high (the topology-only principle is enforced by convention, not cryptography)
- **Symptom:** Nothing prevents a careless code change from querying content fields
- **Suspected cause:** Key infrastructure hasn't been prioritized yet — code discipline has been sufficient so far
- **Attempted:** Test-level enforcement provides partial coverage

### Key distribution channel not confirmed

- **Severity:** medium (design assumes `mind init`, but this needs NLR confirmation)
- **Symptom:** If `mind init` is not the right channel, the distribution model needs redesign
- **Suspected cause:** Mind Protocol's key distribution infrastructure may have constraints we haven't accounted for
- **Attempted:** Escalation marker added to PATTERNS doc

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement (building the encryption layer) or VIEW_Design (choosing cryptographic algorithms)

**Where I stopped:** Doc chain is complete. Design is clear. Implementation has not started. The next step is to confirm the distribution channel with NLR, then select a cryptographic algorithm, then build.

**What you need to understand:**
This module is the HOW for the topology-only principle. The topology_only_principle module explains WHY and WHAT. This module explains the cryptographic mechanism that enforces it. They are complementary — read both before implementing.

**Watch out for:**
- The temptation to over-engineer key management. Start with a simple asymmetric pair and `mind init` distribution. Add complexity (per-session keys, forward secrecy) only when proven necessary.
- Key rotation is a distributed coordination problem. Every citizen brain must re-encrypt with the new key. This takes time and requires monitoring.
- Opt-out detection is subtle: a citizen whose topology is undecryptable might have opted out or might have a stale key. The system must distinguish these cases.

**Open questions I had:**
- What secrets management infrastructure does Mind Protocol use? Vault? AWS KMS? Local file?
- Should the GraphCare public key be signed by a protocol-level authority for authenticity verification?
- What is the expected time for key rotation to propagate across all citizens? (Depends on how often citizens run `mind sync`)

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Created the doc chain for GraphCare's key infrastructure — the dual encryption model that cryptographically enforces the topology-only principle. All four docs are complete. No code exists yet. Several design decisions need your input before implementation can begin.

**Decisions made:**
- Opted for asymmetric encryption with separate key pairs (GraphCare and citizen)
- Key distribution via `mind init` (needs your confirmation)
- Opt-out is unilateral key removal (no GraphCare cooperation needed)
- Key rotation quarterly with transition period

**Needs your input:**
- Is `mind init` the right distribution channel for GraphCare's public key?
- What secrets management infrastructure should hold GraphCare's private key?
- Should we prioritize building this now or continue with code-discipline enforcement?

---

## TODO

### Doc/Impl Drift

- [ ] DOCS→IMPL: Entire module is design-only — no implementation exists yet

### Tests to Run

```bash
# No tests yet — infrastructure not built
# When built: pytest tests/test_key_infrastructure.py
```

### Immediate

- [ ] Confirm key distribution channel with NLR
- [ ] Select cryptographic algorithm (RSA-2048, Ed25519, or other)
- [ ] Design key storage for GraphCare private key

### Later

- [ ] Build key generation tooling
- [ ] Integrate public key into `mind init` bootstrap
- [ ] Build key rotation automation
- IDEA: Key ceremony documentation for when GraphCare generates its first production key pair

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Clear on the design, uncertain on infrastructure details. The model is sound — dual encryption with separate key holders is well-understood cryptography. The unknowns are deployment-specific: where to store the private key, how to hook into `mind init`, how fast key rotation propagates.

**Threads I was holding:**
- The relationship between this module and the topology-only principle (this is the enforcement layer)
- Whether per-session keys add meaningful security over a static key pair (probably v2)
- The opt-out detection problem (undecryptable = opted out? or = stale key?)

**Intuitions:**
Start simple. A single RSA-2048 key pair, distributed through `mind init`, stored in a secrets file, rotated manually at first. Automate after the basic flow works. The cryptographic model is simple; the deployment logistics are the hard part.

**What I wish I'd known at the start:**
The exact capabilities of `mind init` — what it can carry, how often it runs, whether it supports key updates. This would have made the distribution model more concrete.

---

## POINTERS

| What | Where |
|------|-------|
| Topology-only principle | `docs/privacy/topology_only_principle/` |
| Daily health algorithm | `docs/assessment/daily_citizen_health/ALGORITHM_Daily_Citizen_Health.md` |
| Daily health patterns | `docs/assessment/daily_citizen_health/PATTERNS_Daily_Citizen_Health.md` |
| Brain topology reader | `services/health_assessment/brain_topology_reader.py` |
