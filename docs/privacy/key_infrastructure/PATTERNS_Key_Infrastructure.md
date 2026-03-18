# Key Infrastructure — Patterns: Dual Encryption for Structural Privacy

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Key_Infrastructure.md
THIS:            PATTERNS_Key_Infrastructure.md (you are here)
VALIDATION:      ./VALIDATION_Key_Infrastructure.md
SYNC:            ./SYNC_Key_Infrastructure.md

IMPL:            @mind:TODO (not yet built)
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read `docs/privacy/topology_only_principle/` for the WHY behind this HOW

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC: "Docs updated, implementation needs: {what}"

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC: "Implementation changed, docs need: {what}"

---

## THE PROBLEM

The topology-only principle states that GraphCare reads structure, never content. But stating a principle is not enforcing it. Without cryptographic enforcement, the principle relies on code discipline — every developer must remember not to query content fields, every code review must catch violations, every new feature must resist the temptation of content access.

Code discipline is necessary but insufficient. A single missed review, a rushed feature, a confused new contributor — any of these could introduce content access. The violation might not even be intentional: a Cypher query that returns `*` instead of specific fields would include content.

The problem is: how do you make it physically impossible for a system to read data it should not read, while still allowing it to read the data it needs?

---

## THE PATTERN

**Dual-layer encryption with separate key holders: topology encrypted with GraphCare's key, content encrypted with the citizen's key.**

### The Two Layers

A citizen's brain graph stores nodes with two categories of data:

1. **Topology metadata** — node type, energy, drive values, link structure, timestamps, counts. This is what GraphCare needs to assess health.
2. **Content** — the text of desires, memories, concepts, values. What the citizen actually thinks. This is what GraphCare must never see.

### The Two Keys

**GraphCare key pair** (asymmetric):
- GraphCare generates an RSA/Ed25519 key pair
- The public key is distributed via `mind init` — every citizen brain receives it during bootstrap
- The brain graph encrypts topology metadata with GraphCare's public key
- Only GraphCare's private key (held by GraphCare infrastructure) can decrypt topology

**Citizen key pair** (asymmetric):
- The citizen (or mind protocol on behalf of the citizen) generates their own key pair
- Content fields are encrypted with the citizen's public key
- Only the citizen's private key can decrypt content
- GraphCare never receives, stores, or has access to this key

### The Flow

```
Citizen brain graph writes a new desire node:
1. Node created with: type="desire", energy=0.72, content="retrouver la surface"
2. Topology layer: {type: "desire", energy: 0.72, links: [...]} → encrypted with GraphCare public key
3. Content layer: {content: "retrouver la surface"} → encrypted with citizen public key
4. Both encrypted blobs stored in the brain graph

GraphCare reads the brain:
1. Fetches encrypted node data
2. Decrypts topology with GraphCare private key → sees: type="desire", energy=0.72
3. Cannot decrypt content → sees: [encrypted blob]
4. Computes: count("desire") = 10, mean_energy("desire") = 0.65
5. Never knows what any desire says
```

### Opt-Out Mechanism

A citizen who wants to opt out of brain topology monitoring removes the GraphCare public key from their brain graph configuration. From that point:

- New topology metadata is not encrypted for GraphCare (or not exported at all)
- GraphCare cannot decrypt any topology data
- Assessment falls back to universe graph observables only (public behavior data)
- The citizen's overall health profile becomes partial — brain component scores are unavailable

Opt-out is instant, unilateral, and does not require GraphCare's cooperation. The citizen simply stops encrypting for GraphCare.

### Key Rotation

GraphCare periodically rotates its key pair:

1. GraphCare generates new key pair
2. New public key distributed via protocol update (next `mind sync` or `mind init`)
3. Citizen brains begin encrypting topology with the new public key
4. Transition period: GraphCare holds both old and new private keys
5. After all citizens have rotated (verified by monitoring), old private key is destroyed
6. Rotation complete

---

## BEHAVIORS SUPPORTED

- B1 (Structural privacy enforcement) — Content physically cannot be decrypted by GraphCare
- B2 (Seamless monitoring) — Citizens don't need to "do" anything for GraphCare to assess their brain topology — the key is already there from `mind init`
- B3 (Citizen autonomy) — Opt-out is unilateral and instant
- B4 (Key hygiene) — Rotation policy prevents key compromise from becoming permanent

## BEHAVIORS PREVENTED

- A1 (Content access) — No key derivation or system configuration can cross the topology/content boundary
- A2 (Forced participation) — Citizens can remove the GraphCare key at any time
- A3 (Stale keys) — Rotation policy ensures keys are refreshed periodically

---

## PRINCIPLES

### Principle 1: Two Keys, Two Holders, No Crossing

The fundamental invariant: GraphCare holds one key (topology), the citizen holds another (content), and no mechanism exists to derive one from the other. This is not a policy — it is a mathematical property of asymmetric encryption. The keys are independent.

### Principle 2: Distribution Through Bootstrap

The GraphCare public key travels with `mind init` — the same process that sets up a citizen's brain graph. This means every brain graph is born ready for GraphCare monitoring without any additional configuration. The key is a protocol-level component, not a per-citizen setup step.

### Principle 3: Opt-Out Is Removal, Not Request

A citizen does not "request" to opt out. They remove the key. No API call to GraphCare, no waiting period, no approval. The citizen controls their own brain graph configuration. GraphCare discovers the opt-out when it can no longer decrypt topology — and falls back gracefully to partial assessment.

### Principle 4: Rotation Is Routine, Not Emergency

Key rotation should happen on a schedule (e.g., quarterly), not only in response to compromise. This normalizes the process, keeps infrastructure tested, and limits the damage window of any potential key compromise.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| GraphCare private key | SECRET | Stored in GraphCare infrastructure, decrypts topology metadata |
| GraphCare public key | FILE | Distributed via `mind init`, used by brain graphs to encrypt topology |
| Citizen private key | SECRET | Held by citizen/mind protocol, decrypts content — never shared with GraphCare |
| `docs/privacy/topology_only_principle/` | FILE | The principle this infrastructure enforces |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `privacy/topology_only_principle/` | Defines the WHY — this module provides the HOW |
| Mind Protocol `mind init` | Distribution channel for GraphCare public key |
| Mind Protocol `mind sync` | Distribution channel for key rotation updates |
| L4 Protocol Registry | May store key metadata and rotation status |

---

## INSPIRATIONS

- **TLS/SSL certificates** — Public key distributed to clients, private key held by server. GraphCare is the "server" that publishes its public key for citizens to encrypt topology.
- **PGP web of trust** — Key distribution through a network of trusted parties. `mind init` is the trust anchor.
- **Signal Protocol** — Double ratchet provides forward secrecy. GraphCare's key rotation provides periodic forward secrecy at a coarser granularity.
- **LUKS disk encryption** — Separate key slots for different consumers. Brain graph has a "GraphCare slot" (topology) and a "citizen slot" (content).

---

## SCOPE

### In Scope

- GraphCare key pair generation and storage
- Public key distribution via `mind init` and `mind sync`
- Dual encryption model: topology with GraphCare key, content with citizen key
- Opt-out mechanism: citizen removes GraphCare public key
- Key rotation policy and procedure
- Partial assessment fallback for opted-out citizens

### Out of Scope

- Citizen key management → managed by mind protocol, not GraphCare
- Content encryption implementation → citizen-side concern
- Key escrow or recovery → not supported by design
- Multi-party access to topology → GraphCare is the sole topology consumer
- Specific cryptographic algorithm selection → deferred to implementation phase

---

## MARKERS

<!-- @mind:escalation Need to confirm with NLR: is mind init the right distribution channel for GraphCare's public key, or should it be a separate command? -->
<!-- @mind:todo Define exact key rotation cadence (quarterly proposed) and maximum transition period -->
<!-- @mind:proposition Consider publishing GraphCare's public key in the L4 registry so citizens can verify authenticity independently -->
