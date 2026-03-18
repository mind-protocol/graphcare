# OBJECTIVES — Brain Scan

```
STATUS: DESIGNING
CREATED: 2026-03-18
VERIFIED: —
```

---

## CHAIN

```
THIS:            OBJECTIVES_Brain_Scan.md (you are here - START HERE)
PATTERNS:       ./PATTERNS_Brain_Scan.md
BEHAVIORS:      ./BEHAVIORS_Brain_Scan.md
ALGORITHM:      ./ALGORITHM_Brain_Scan.md
VALIDATION:     ./VALIDATION_Brain_Scan.md
IMPLEMENTATION: ./IMPLEMENTATION_Brain_Scan.md
SYNC:           ./SYNC_Brain_Scan.md

IMPL:           services/brain_scan/brain_scan_data_extractor.py
```

**Read this chain in order before making changes.** Each doc answers different questions. Skipping ahead means missing context.

---

## PRIMARY OBJECTIVES (ranked)

1. **O1: Make brain state visible** — Turn topology data (220+ nodes, 457+ links) into an intuitive 3D visualization that a human or agent can rotate, zoom, and explore. A health score of 23/100 means nothing without seeing the structural reasons behind it. The visualization is the explanation.

2. **O2: Anatomy-based layering** — Position nodes in brain-like layers that map semantic type to spatial position. Stem (z=0.0-0.2) holds process nodes — the basic machinery. Limbic (z=0.2-0.5) holds desires and narratives — drives and emotions. Cortex (z=0.5-1.0) holds values and concepts — higher reasoning. This spatial metaphor makes complex topology legible at a glance.

3. **O3: Actionable insight** — The visualization should reveal what GraphCare health scores mean in structural terms. A disconnected cortex, an overloaded stem, a limbic region with no links to values — these visual patterns translate abstract numbers into understanding. The scan is the bridge between data and decision.

4. **O4: Pre-computed, not live** — Generate the scan offline (FalkorDB query + positioning), then explore interactively in the browser. This separates the heavy computation from the lightweight interaction, avoids FalkorDB load during exploration, and produces standalone HTML files that can be shared and archived.

## NON-OBJECTIVES

- Real-time streaming — we do not stream brain state changes live. The scan is a snapshot.
- Force-directed graph layout — we use anatomy-layer positioning, not physics-based spring layouts. The metaphor is biology, not network science.
- Replacing health assessment scores — the brain scan visualizes structure; it does not compute health metrics. Health scoring is a separate module.

## TRADEOFFS (canonical decisions)

- When visual clarity conflicts with completeness, choose visual clarity. A legible scan of 80% of the brain is more useful than a cluttered scan of 100%.
- When topology depth conflicts with content privacy, choose topology. We read structure (types, weights, edges), never content or synthesis fields. The kidney sees the shape, not the substance.
- When static pre-computation conflicts with live rendering, choose static-then-explore. One FalkorDB query per scan, then infinite browser exploration without further database load.

## SUCCESS SIGNALS (observable)

- A generated HTML file opens in a browser and shows a recognizable brain-like 3D structure with visible layers
- Layer toggles correctly show/hide stem, limbic, and cortex regions
- Hovering a node displays its type, label, weight, and energy — never its content
- A scan of 220 nodes + 457 links renders and remains interactive (smooth rotation/zoom)

---

## MARKERS

<!-- @mind:todo Establish quantitative success criteria for render performance (target FPS, max node count before degradation) -->
