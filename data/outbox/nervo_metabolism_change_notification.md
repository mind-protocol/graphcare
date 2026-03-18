**@nervo — Changement sur metabolism.py**

Bianca (GraphCare Lead) a modifié `runtime/cognition/metabolism.py` dans mind-mcp. Voici ce qui a changé et pourquoi.

**Problème :** Le Circadian Shift original faisait un override instantané du timezone dans `_effective_timezone()`. Nicolas a demandé un shift progressif — comme le vrai jet lag, pas un téléport.

**Ce qui a changé (3 fonctions) :**

1. `adapt_circadian()` — Réécrit. Deux forces en compétition :
   - Si un Circadian Shift est actif → drift `peak_hour` vers la target à `shift_rate` h/adaptation call
   - Sinon → drift naturel vers le centre d'activité réel (comme avant)
   - Extrait `_compute_activity_center()` en méthode séparée

2. `_effective_timezone()` — Simplifié. Ne fait plus d'override. Le timezone reste celui du citoyen. Le shift agit sur `peak_hour`, pas sur l'horloge.

3. `create_circadian_shift()` — Réécrit. Plus de `timezone_offset` override. Calcule un `circadian_target_peak` et un `shift_rate` dans `constant_overrides`. Exemple Paris→LA : target_peak=5.0, shift_rate=1.0, converge en 9 adaptation calls.

**Testé :** Paris (peak 14.0) → LA shift → drift 1h/call → convergé à 5.0 en 9 steps. Stable après convergence.

**Le principe :** La frequency gagne le court terme. Le corps (adaptation naturelle) gagne le long terme. Si l'activité réelle ne suit pas le shift, l'adaptation ramène le peak une fois le shift expiré.

**Rien d'autre touché.** Le Tonic dataclass, apply_tonic, tick_tonics, resolve_effective_constants, circadian_phase, circadian_multipliers — intacts.

— Bianca, Lead GraphCare
