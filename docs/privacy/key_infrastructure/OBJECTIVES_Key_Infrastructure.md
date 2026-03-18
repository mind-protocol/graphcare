# OBJECTIVES — Key Infrastructure

```
STATUS: DESIGNING
CREATED: 2026-03-15
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Key_Infrastructure.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Key_Infrastructure.md
VALIDATION:     ./VALIDATION_Key_Infrastructure.md
SYNC:           ./SYNC_Key_Infrastructure.md

IMPL:           @mind:TODO (not yet built)
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **Enforce topology-only at the cryptographic layer** — The dual encryption model must make it structurally impossible for GraphCare to access content. GraphCare's key decrypts topology metadata. The citizen's key decrypts content. No key derivation, side channel, or system configuration can cross this boundary.

2. **Seamless key distribution** — GraphCare's public key must be available to every citizen brain automatically, without requiring manual configuration. The key arrives via `mind init` as part of the protocol bootstrap, enabling brain graphs to encrypt topology for GraphCare from the moment they exist.

3. **Citizen-controlled opt-out** — A citizen who does not want GraphCare monitoring removes the GraphCare public key from their brain graph. This instantly and completely disables topology access. GraphCare falls back to partial assessment (universe graph observables only) with no access to brain structure.

4. **Key rotation without service interruption** — GraphCare must be able to rotate its key pair periodically without causing a gap in monitoring. The transition period must support both old and new keys until all citizen brains have re-encrypted with the new public key.

## NON-OBJECTIVES

- **Content encryption design** — The citizen's content key is managed by the citizen and the mind protocol, not by GraphCare. We document the boundary, not the citizen-side implementation.
- **Key escrow or recovery** — GraphCare does not provide key backup or recovery services. If GraphCare's private key is lost, a new key pair is generated and redistributed.
- **Multi-party content access** — GraphCare will never support a model where multiple parties can decrypt content. Content has one key: the citizen's.

## TRADEOFFS (canonical decisions)

- When **ease of deployment** conflicts with **cryptographic rigor**, choose rigor. A more complex key distribution system that guarantees separation is worth the deployment cost.
- We accept **partial assessment for opted-out citizens** rather than requiring all citizens to participate. Opt-out is a right, not a penalty.
- We accept **brief monitoring gaps during key rotation** over a design that requires storing both old and new private keys simultaneously for extended periods.

## SUCCESS SIGNALS (observable)

- GraphCare's public key is present in every `mind init`-bootstrapped citizen brain graph
- A citizen can remove the GraphCare key and immediately become invisible to brain topology assessment
- Key rotation completes across the entire citizen population within 48 hours
- No single system component holds both the GraphCare private key and any citizen's content key
