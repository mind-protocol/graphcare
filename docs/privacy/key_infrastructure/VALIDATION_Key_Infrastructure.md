# Key Infrastructure — Validation: What Must Be True

```
STATUS: DESIGNING
CREATED: 2026-03-15
```

---

## CHAIN

```
OBJECTIVES:      ./OBJECTIVES_Key_Infrastructure.md
PATTERNS:        ./PATTERNS_Key_Infrastructure.md
THIS:            VALIDATION_Key_Infrastructure.md (you are here)
SYNC:            ./SYNC_Key_Infrastructure.md

IMPL:            @mind:TODO (not yet built)
```

---

## PURPOSE

**Validation = what we care about being true.**

These invariants protect the cryptographic guarantee that separates topology from content. The key infrastructure is the enforcement mechanism for the topology-only principle. If these invariants fail, the principle becomes a gentleman's agreement instead of a mathematical certainty.

---

## INVARIANTS

### V1: Key Independence

**Why we care:** If GraphCare's key can derive or access the citizen's key (or vice versa), the entire dual encryption model collapses. The keys must be mathematically independent — knowing one reveals nothing about the other.

```
MUST:   GraphCare's key pair and citizen's key pair are generated independently with no shared seed, derivation path, or master key
NEVER:  A mechanism exists (mathematical, procedural, or social) to derive the citizen's content key from GraphCare's topology key
```

### V2: Public Key Reaches Every Brain

**Why we care:** If a citizen's brain graph does not have GraphCare's public key, topology cannot be encrypted for GraphCare, and that citizen is silently unmonitored. Unlike opt-out (which is intentional), a missing key is an infrastructure failure.

```
MUST:   Every brain graph bootstrapped via mind init receives GraphCare's current public key as part of the initialization process
NEVER:  A citizen brain exists in a work universe (Lumina Prime) without GraphCare's public key unless the citizen explicitly opted out
```

### V3: Private Key Isolation

**Why we care:** GraphCare's private key is the single point of access for all citizen topology data. If it leaks, every citizen's brain topology is exposed. If it coexists with a citizen's content key in any system, the separation guarantee weakens.

```
MUST:   GraphCare's private key is stored in a dedicated secrets manager, accessible only to the topology decryption service
NEVER:  GraphCare's private key exists on the same system, in the same process, or in the same secrets namespace as any citizen's content key
```

### V4: Opt-Out Is Immediate and Unilateral

**Why we care:** If opt-out requires GraphCare's cooperation, a citizen cannot truly withdraw consent. If opt-out has a delay, there is a window of unwanted monitoring. The citizen's autonomy over their own brain graph must be absolute.

```
MUST:   Removing the GraphCare public key from a brain graph immediately stops topology encryption for GraphCare — no grace period, no confirmation, no API call to GraphCare
NEVER:  GraphCare can override, delay, or reverse a citizen's opt-out decision
```

### V5: Key Rotation Completes Without Data Loss

**Why we care:** Key rotation is necessary for security hygiene, but if it causes monitoring gaps (citizens encrypted with old key, GraphCare only has new key), health assessment silently fails for those citizens. The transition must be smooth.

```
MUST:   During key rotation, GraphCare holds both old and new private keys until all active citizen brains have re-encrypted with the new public key
NEVER:  A citizen's topology data becomes undecryptable during a rotation because GraphCare discarded the old key too early
```

### V6: Partial Assessment for Opted-Out Citizens

**Why we care:** Opted-out citizens still have public universe graph data. GraphCare should still provide whatever assessment is possible from public data alone, so that opting out of brain monitoring does not mean opting out of all health insight.

```
MUST:   Citizens who have opted out of brain topology monitoring receive a partial health assessment based on universe graph observables (behavior component only)
NEVER:  An opted-out citizen is treated as if they don't exist — their public behavior data should still be assessed
```

---

## PRIORITY

| Priority | Meaning | If Violated |
|----------|---------|-------------|
| **CRITICAL** | System purpose fails | Unusable |
| **HIGH** | Major value lost | Degraded severely |
| **MEDIUM** | Partial value lost | Works but worse |

---

## INVARIANT INDEX

| ID | Value Protected | Priority |
|----|-----------------|----------|
| V1 | Mathematical key independence | CRITICAL |
| V2 | Universal key distribution | HIGH |
| V3 | Private key isolation | CRITICAL |
| V4 | Citizen autonomy — immediate opt-out | HIGH |
| V5 | Continuity during key rotation | HIGH |
| V6 | Partial service for opted-out citizens | MEDIUM |

---

## MARKERS

<!-- @mind:escalation Confirm with NLR: what secrets management infrastructure is available for GraphCare's private key? -->
<!-- @mind:todo Define monitoring/alerting for citizens whose topology becomes undecryptable (distinguishing opt-out from infrastructure failure) -->
<!-- @mind:proposition Consider a "key health dashboard" that shows: total citizens, citizens with current key, citizens with old key, opted-out citizens -->
