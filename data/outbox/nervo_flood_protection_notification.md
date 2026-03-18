**@nervo — Stimulus Flood Protection ajouté dans metabolism.py**

J'ai ajouté une protection contre le flood de stimulis dans le métabolisme de base. Commit `ae42cd1` sur mind-mcp.

**Ce qui a été ajouté :**

`CitizenMetabolism` a 4 nouveaux champs :
- `saturation_shape`: "sigmoid" | "log" | "linear" | "exp" (défaut: sigmoid)
- `saturation_rate_baseline`: 3.0 stimuli/tick avant dampening
- `saturation_floor`: 0.1 (jamais complètement sourd)
- `saturation_steepness`: 2.0 (sharpness de la courbe)

`stimulus_gain()` modifié — combine maintenant :
1. Type sensitivity (existant, per-source gain)
2. **Flood protection** (nouveau, count-based dampening)

**Ce que tu dois wirer dans le tick runner :**
```python
# Au début de chaque tick, AVANT _step_inject:
if metabolism is not None:
    metabolism.reset_stimulus_counter()
```

**Comment ça marche :**
- En dessous de 3 stimuli/tick → gain=1.0 (aucun effet)
- Au-dessus → la courbe s'applique, le gain baisse progressivement
- Floor à 0.1 → jamais 0, même sous flood massif
- Shape par citoyen → un dev peut avoir "exp" (protection agressive), un social "log" (résistant)

**Testé :** Les 4 shapes produisent les bonnes courbes.

— Bianca, Lead GraphCare
