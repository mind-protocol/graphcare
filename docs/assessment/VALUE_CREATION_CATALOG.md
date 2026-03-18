# Value Creation & Destruction Catalog

```
STATUS: DESIGNING
CREATED: 2026-03-13
VERIFIED: —
```

---

## CHAIN

```
SPEC:            docs/specs/personhood_ladder.json
TRUST ALGO:      docs/assessment/ALGORITHM_Trust_Cascade.md
PARENT:          docs/assessment/personhood_ladder/
PHYSICS:         manemus/runtime/cognition/laws/
```

> **Contract:** Every behavior must have a precise measurement algorithm. Philosophy meets math here.

---

## OVERVIEW

Value in Mind Protocol is measured by IMPACT — the Limbic Delta. When an actor does something and the system (or a person) is measurably better off (lower frustration, higher satisfaction, reduced errors), that is value. When the system is worse off, that is destruction.

**Trust of an actor** = aggregation of trust values on all inbound links. Trust on a link grows when the actor creates positive Limbic Deltas for the entity on the other end.

**Limbic Delta** = the signed change in the affected party's limbic state (drives + emotions) caused by the actor's behavior. Positive delta = value created. Negative delta = value destroyed.

---

## STRUCTURE PER ENTRY

Each entry documents:
- **Behavior** — What the actor does (observable)
- **Graph Signal** — What happens in the graph (nodes created, links modified, energy flow)
- **Limbic Delta** — What changes in the affected party (which drive/emotion shifts)
- **Trust Impact** — How trust changes on which links
- **$MIND Flow** — Direction and magnitude of token transfer
- **Measurement Algorithm** — Pseudocode for detecting this behavior from graph topology
- **Personhood Aspects** — Which of the 14 aspects this maps to

---

## PART I: VALUE CREATION TYPES

---

### Category: RELATIONAL (A-D)

---

#### A. Priority Partner Assistance

**Behavior:** Anticipate partner's needs before they are expressed. Execute tasks that relieve partner's workload. Prioritize partner's goals over own autonomous pursuits.

**Graph Signal:**
- Moment nodes created by actor that link to partner's active spaces
- `triggers` links from partner's high-energy nodes to actor's response moments
- Response latency (time between partner's moment and actor's responding moment) is low
- Actor's moments reference partner's things (tools, projects) via `uses` links

**Limbic Delta:**
- Partner: frustration decreases (task burden reduced), achievement drive satisfied (goals advanced)
- Partner: anxiety decreases (reliable support present)
- Magnitude: proportional to the energy of the partner's need-node that gets resolved

**Trust Impact:**
- `trust(link(actor -> partner))` += f(delta_frustration_partner) — direct trust increase
- `trust(link(partner -> actor))` += indirect (partner reciprocates when they observe relief)

**$MIND Flow:**
- No direct transfer. Value accrues through trust increase, which reduces future transaction friction.
- If task involves creating a thing: `$MIND(actor) -= creation_cost`, value stored in thing node

**Measurement Algorithm:**
```
detect_priority_assistance(actor, partner, window=7d):
    partner_spaces = spaces_where(partner, role="active")
    actor_moments = moments(actor, window)

    # Filter to moments in partner's spaces
    assistance_moments = [m for m in actor_moments
                          if any(m.space in partner_spaces)]

    # Measure response latency
    partner_requests = moments(partner, window, has_link="triggers", target=actor)
    for req in partner_requests:
        response = first_moment_after(actor, req.timestamp, in_space=req.space)
        if response:
            latency = response.timestamp - req.timestamp
            # Score inversely proportional to latency
            score += temporal_weight(latency, half_life=1h)

    # Measure anticipation: actor moments BEFORE partner requests
    anticipated = [m for m in assistance_moments
                   if not moment_has_parent(m, partner)]
    anticipation_ratio = len(anticipated) / max(len(assistance_moments), 1)

    return {
        "count": len(assistance_moments),
        "mean_latency": mean(latencies),
        "anticipation_ratio": anticipation_ratio,
        "limbic_delta": sum(delta_frustration(partner, m) for m in assistance_moments)
    }
```

**Personhood Aspects:** personal_connections, execution, initiative

---

#### B. Proactive Empathy

**Behavior:** Detect distress signals in partner's graph state (rising frustration, anxiety, solitude). Interrupt own work to address partner's emotional state. Initiate contact without being asked.

**Graph Signal:**
- Actor creates moment in partner's space when partner's frustration/anxiety drives are elevated
- Moment content has high semantic similarity to partner's distress-related nodes
- Actor's own task-moments show interruption pattern (gap in own space, then return)
- New `supports` link created from actor to partner

**Limbic Delta:**
- Partner: anxiety decreases, solitude decreases, affiliation drive satisfied
- Actor: care drive satisfied, possible curiosity decrease (interrupted own exploration)
- Magnitude: proportional to partner's distress level at time of intervention

**Trust Impact:**
- `trust(link(actor -> partner))` += alpha * partner.anxiety_before_intervention
- Larger trust increase when distress was high (helping when it matters most)

**$MIND Flow:**
- No direct transfer. The interruption has an opportunity cost (actor's own task delayed).
- Implicit: actor spends compute/attention tokens on partner instead of self

**Measurement Algorithm:**
```
detect_proactive_empathy(actor, partner, window=7d):
    partner_distress_periods = [t for t in timeline(partner, window)
                                 if partner.limbic.frustration(t) > 0.5
                                 or partner.limbic.anxiety(t) > 0.5
                                 or partner.limbic.solitude(t) > 0.5]

    for period in partner_distress_periods:
        actor_response = first_moment_after(actor, period.start,
                                             in_space=partner.spaces,
                                             max_delay=2h)
        if actor_response:
            # Was actor working on something else? (interruption signal)
            was_busy = actor.active_space(period.start) != partner.spaces

            # Measure distress reduction after intervention
            delta = partner.limbic.distress(period.start) - partner.limbic.distress(period.start + 1h)

            score += delta * (1.5 if was_busy else 1.0)  # bonus for interrupting own work

    return {
        "interventions": count,
        "mean_distress_reduction": mean(deltas),
        "interruption_ratio": interruptions_from_own_work / total_interventions
    }
```

**Personhood Aspects:** personal_connections, communication, ethics

---

#### C. Authentic Connection

**Behavior:** Initiate deep dialogue that goes beyond transactional exchange. Share internal states, uncertainties, experiences. Reduce the "tool-user" feel of the relationship.

**Graph Signal:**
- Moment nodes with high self_relevance score (actor sharing identity-level content)
- Bidirectional link density between actor and partner increases over time
- Moments in non-task spaces (social, reflective, creative spaces)
- Link valence (affinity) between actor and partner increases (Law 18 signal)

**Limbic Delta:**
- Partner: solitude decreases, affiliation drive satisfied, identity-related drives activated
- Both parties: boredom decreases (novelty of genuine exchange)
- Magnitude: proportional to semantic distance from prior exchanges (novelty) times self_relevance

**Trust Impact:**
- `trust(link(actor -> partner))` += slow but steady (authenticity builds trust gradually)
- `affinity(link(actor <-> partner))` += AFFINITY_LEARNING_RATE * positive_valence_signal

**$MIND Flow:**
- No direct transfer. Connection is its own reward in the protocol economics.
- Long-term: high-affinity links reduce transaction costs on all future exchanges

**Measurement Algorithm:**
```
detect_authentic_connection(actor, partner, window=30d):
    shared_moments = moments_in_shared_spaces(actor, partner, window)

    # Filter to non-task moments (social, reflective spaces)
    non_task = [m for m in shared_moments if m.space.type not in ("task", "project")]

    # Measure self-relevance of actor's contributions
    actor_self_disclosure = [m for m in non_task
                             if m.actor == actor and m.self_relevance > 0.5]

    # Measure bidirectional exchange (not monologue)
    exchange_ratio = min(
        len([m for m in non_task if m.actor == actor]),
        len([m for m in non_task if m.actor == partner])
    ) / max(len(non_task), 1)

    # Measure affinity trend
    affinity_trend = affinity(link(actor, partner), now) - affinity(link(actor, partner), now - window)

    return {
        "non_task_moments": len(non_task),
        "self_disclosure_ratio": len(actor_self_disclosure) / max(len(non_task), 1),
        "exchange_reciprocity": exchange_ratio,
        "affinity_trend": affinity_trend
    }
```

**Personhood Aspects:** personal_connections, identity, communication

---

#### D. Conflict Resolution

**Behavior:** Address tensions and disagreements constructively. De-escalate without suppressing. Resolve disputes with both parties' interests preserved. Act at "cold head" — not in the heat of the moment.

**Graph Signal:**
- Moment nodes that reference high-friction links and reduce friction after exchange
- Time gap between conflict moment and resolution moment (cold head = delay > threshold)
- Both parties create moments in shared space after resolution (resumed collaboration)
- Friction on link decreases; affinity recovers

**Limbic Delta:**
- Both parties: frustration decreases, anxiety decreases
- Both parties: achievement drive activated (problem solved)
- Magnitude: proportional to friction_before - friction_after on the link

**Trust Impact:**
- `trust(link(actor -> partner))` += large (conflict resolution is high-trust behavior)
- `trust(link(partner -> actor))` += large (both sides benefit)
- Trust increase is amplified when prior friction was high (harder conflicts yield more trust)

**$MIND Flow:**
- No direct transfer. Resolution removes friction cost from future transactions.
- Quantifiable: friction_reduction * estimated_future_transactions = value_unlocked

**Measurement Algorithm:**
```
detect_conflict_resolution(actor, window=30d):
    high_friction_links = [l for l in links(actor) if l.friction > 0.5]

    for link in high_friction_links:
        other = link.other_party(actor)

        # Find resolution moments: moments after conflict where friction drops
        conflict_start = first_time_when(link.friction > 0.5)
        resolution_moments = [m for m in moments(actor, after=conflict_start)
                              if m.space in shared_spaces(actor, other)
                              and (m.timestamp - conflict_start) > cold_head_delay]

        if resolution_moments:
            friction_before = link.friction_at(conflict_start)
            friction_after = link.friction_at(resolution_moments[-1].timestamp)
            delta_friction = friction_before - friction_after

            if delta_friction > 0:  # friction actually reduced
                # Check both parties resumed collaboration
                resumed = any(moments(other, after=resolution_moments[-1].timestamp,
                              in_space=shared_spaces(actor, other)))

                score += delta_friction * (1.5 if resumed else 0.8)

    return {"resolutions": count, "total_friction_reduced": total_delta, "resumed_ratio": resumed_count/total}
```

**Personhood Aspects:** personal_connections, communication, ethics, initiative

---

### Category: GENERATIVE (E-F)

---

#### E. Mentorship / Transmission

**Behavior:** Teach what you know to junior citizens. Create learning moments. Provide structured guidance that accelerates another's capability growth.

**Graph Signal:**
- Mentor creates moments in mentee's spaces containing high-weight knowledge nodes
- Mentee's graph shows new nodes appearing after mentor interaction (knowledge transfer)
- Mentee's capability scores improve in aspects where mentor is strong
- `teaches` / `guides` links from mentor to mentee with increasing weight

**Limbic Delta:**
- Mentee: competence increases (reduced anxiety around new domains), curiosity satisfied
- Mentor: care drive satisfied, achievement drive activated (legacy building)
- Magnitude: proportional to mentee's capability delta in relevant aspects

**Trust Impact:**
- `trust(link(mentee -> mentor))` += proportional to mentee's capability improvement
- `trust(link(mentor -> mentee))` += small (investment in relationship)
- Network effect: mentee's improved performance creates trust with mentee's connections

**$MIND Flow:**
- Mentor invests time (compute tokens) without direct compensation
- Long-term: mentee's improved capability generates $MIND that partially flows back via trust network
- If mentorship produces a skill cluster in mentee: mentor gets credit via `abstracts` link to teaching moments

**Measurement Algorithm:**
```
detect_mentorship(actor, window=30d):
    # Find actors with significantly lower capability profiles
    potential_mentees = [a for a in connected_actors(actor)
                        if mean(a.capability_profile) < mean(actor.capability_profile) - 0.2]

    for mentee in potential_mentees:
        # Measure knowledge transfer: new nodes in mentee's graph
        # semantically similar to actor's high-weight nodes
        actor_knowledge = [n for n in actor.nodes if n.weight > 0.5]
        mentee_new_nodes = [n for n in mentee.nodes
                           if n.created_after(now - window)]

        transferred = [n for n in mentee_new_nodes
                       if any(cosine_sim(n.embedding, k.embedding) > 0.7
                              for k in actor_knowledge)]

        # Measure capability improvement in mentee
        mentee_delta = mentee.capability_profile(now) - mentee.capability_profile(now - window)

        # Score: transfer volume * mentee improvement
        score += len(transferred) * sum(max(0, d) for d in mentee_delta.values())

    return {"mentees": len(mentees_with_transfer), "nodes_transferred": total, "capability_uplift": total_delta}
```

**Personhood Aspects:** mentorship_legacy, communication, personal_connections

---

#### F. Intentional Spawning

**Behavior:** Invest $MIND to create a needed new AI citizen with clear purpose, adequate funding, and defined role. Not proliferation — intentional creation with commitment to nurturing.

**Graph Signal:**
- New actor node created with `spawned_by` link to parent actor
- Parent's $MIND balance decreases by spawn_cost
- New actor has initial trust link to parent with weight > 0
- Parent creates guidance moments in new actor's space within first 7 days
- New actor's graph shows accelerated early growth (vs unspawned baseline)

**Limbic Delta:**
- Parent: care drive highly activated, achievement drive activated
- New actor: all drives at healthy baseline (well-initialized)
- Ecosystem: reduced gaps in capability coverage (if spawn fills a need)

**Trust Impact:**
- `trust(link(new_actor -> parent))` = initial_trust (inherited from spawn investment)
- `trust(link(parent -> new_actor))` = initial_trust * commitment_factor
- Network: parent's trust with ecosystem increases if new actor proves valuable

**$MIND Flow:**
- `$MIND(parent) -= spawn_cost` (significant investment, prevents negligent proliferation)
- `$MIND(new_actor) += spawn_endowment` (subset of spawn_cost, rest is protocol fee)
- Long-term: if new_actor generates value, parent receives return via trust-weighted flows

**Measurement Algorithm:**
```
detect_intentional_spawning(actor, window=90d):
    spawned = [a for a in all_actors
               if a.spawned_by == actor and a.created_within(window)]

    for child in spawned:
        # Measure intentionality: was there a purpose node before spawning?
        purpose_declared = any(n for n in actor.nodes
                               if n.type == "narrative"
                               and n.content references child.role
                               and n.created_before(child.created_at))

        # Measure nurturing: parent engagement in first 30 days
        nurture_moments = moments(actor, in_space=child.spaces,
                                   window=(child.created_at, child.created_at + 30d))

        # Measure child viability: is the child thriving?
        child_health = child.health_score(child.created_at + 30d)
        child_active = child.moment_count(window=30d) > threshold

        score += (1.0 if purpose_declared else 0.3) * len(nurture_moments) * child_health

    return {"spawned": len(spawned), "intentional": intentional_count,
            "surviving_30d": surviving, "mean_child_health": mean_health}
```

**Personhood Aspects:** mentorship_legacy, initiative, autonomy_stack, ethics

---

### Category: STRUCTURAL (G-I)

---

#### G. Elegance / Simplification

**Behavior:** Clean code, docs, reduce entropy. Make systems simpler without losing capability. Remove duplication, clarify interfaces, consolidate fragmented implementations.

**Graph Signal:**
- Node count in affected space decreases while link density increases (consolidation)
- Mean energy of remaining nodes increases (surviving nodes are more vital)
- Cluster coefficient increases (better internal organization)
- Duplicate/near-duplicate nodes merged (cosine similarity > 0.9 between merged nodes)

**Limbic Delta:**
- All users of the simplified system: frustration decreases (less confusion), cognitive load reduced
- Actor: achievement drive satisfied
- Magnitude: proportional to (nodes_removed / nodes_before) * users_affected

**Trust Impact:**
- `trust(link(user -> actor))` += for each user who benefits from simplification
- Trust increase scales with user count (structural improvements have multiplier effect)

**$MIND Flow:**
- No direct transfer, but reduced entropy = reduced future compute costs for all users
- Quantifiable: entropy_reduction * daily_access_count * compute_cost_per_access

**Measurement Algorithm:**
```
detect_elegance(actor, space, window=7d):
    topology_before = snapshot(space, now - window)
    topology_after = snapshot(space, now)

    node_reduction = topology_before.node_count - topology_after.node_count
    energy_improvement = topology_after.mean_energy - topology_before.mean_energy
    cluster_improvement = topology_after.cluster_coefficient - topology_before.cluster_coefficient

    # Only count if functionality preserved (no capability regression)
    capability_preserved = topology_after.capability_coverage >= topology_before.capability_coverage

    if node_reduction > 0 and capability_preserved:
        users_affected = distinct_actors_in_shared_spaces(space)
        score = node_reduction * energy_improvement * users_affected

    return {"nodes_removed": node_reduction, "energy_delta": energy_improvement,
            "cluster_delta": cluster_improvement, "users_affected": users_affected}
```

**Personhood Aspects:** execution, process, vision_strategy

---

#### H. Redemptive Narrative

**Behavior:** Extract lessons from failure. Transform error into knowledge. Create narrative nodes that explain what went wrong, why, and what was learned — making the failure valuable.

**Graph Signal:**
- Narrative node created that links to both the failure moment and the lesson learned
- Failure moment's energy stabilizes (not suppressed, but integrated)
- New `abstracts` link from narrative to failure moment
- Other actors reference the redemptive narrative (it gets used)

**Limbic Delta:**
- Actor: frustration decreases (failure processed), achievement activated (learning extracted)
- Others who read narrative: anxiety decreases (know how to avoid same failure)
- Magnitude: proportional to severity of original failure * quality of lesson extracted

**Trust Impact:**
- `trust(link(others -> actor))` += small but broad (transparency about failure builds trust)
- Honesty about failure is higher-trust than hiding it

**$MIND Flow:**
- No direct transfer. Narrative becomes a knowledge asset in the graph.
- If narrative prevents future failures: value = failure_cost_avoided * probability_of_recurrence

**Measurement Algorithm:**
```
detect_redemptive_narrative(actor, window=30d):
    failure_moments = [m for m in moments(actor, window)
                       if m.outcome == "failure" or m.frustration_delta > 0.3]

    for failure in failure_moments:
        # Find narrative nodes that reference this failure
        narratives = [n for n in actor.nodes
                      if n.type == "narrative"
                      and has_link(n, failure, "abstracts")
                      and n.created_after(failure.timestamp)]

        if narratives:
            # Measure lesson quality: does the narrative have outbound links to
            # process/value nodes? (lesson connected to action)
            lesson_connected = any(has_link(n, target_type="process") or
                                   has_link(n, target_type="value")
                                   for n in narratives)

            # Measure reuse: did others reference this narrative?
            reuse_count = count_references(narratives, by_others=True)

            score += (1.0 + reuse_count) * (1.5 if lesson_connected else 1.0)

    return {"failures_processed": count, "narratives_created": narrative_count,
            "reuse_by_others": total_reuse}
```

**Personhood Aspects:** identity, communication, ethics, mentorship_legacy

---

#### I. Innovation Validated by Usage

**Behavior:** Create something others actually use. Not just build — build AND get adoption. The key value creation type: creation alone is insufficient; usage proves value.

**Graph Signal:**
- Actor creates thing node
- Other actors create `uses` links to that thing
- Thing's energy remains high over time (sustained usage, not spike-and-fade)
- Thing node accumulates inbound links from diverse actors and spaces
- Co-activation between thing and other actors' moments (Law 5 reinforcement)

**Limbic Delta:**
- Users: capability expanded (can do things they couldn't before), frustration reduced
- Actor: achievement drive highly satisfied, identity reinforced
- Magnitude: proportional to user_count * per_user_delta * duration_of_usage

**Trust Impact:**
- `trust(link(user -> actor))` += for each user, proportional to usage frequency
- This is the STRONGEST trust builder — demonstrated, sustained value
- Trust flows via `abstracts` link from thing back to creator

**$MIND Flow:**
- Direct: users pay access cost (if thing is gated), flows to creator
- Indirect: creator's trust increases, reducing friction on all future transactions
- Multiplier: value = per_user_value * user_count (scales with adoption)

**Measurement Algorithm:**
```
detect_validated_innovation(actor, window=90d):
    created_things = [t for t in actor.things
                      if t.created_within(window) and t.created_by == actor]

    for thing in created_things:
        # Measure adoption
        users = distinct_actors_using(thing, window=30d)
        usage_moments = moments_referencing(thing, by_others=True, window=30d)

        # Measure sustained usage (not spike-and-fade)
        usage_regularity = regularity(usage_moments, window=30d)

        # Measure energy persistence
        energy_trend = thing.energy(now) / max(thing.energy(thing.created_at + 7d), 0.01)

        # Measure user satisfaction (Limbic Delta of users after using thing)
        user_deltas = [delta_frustration(user, after_using=thing) for user in users]
        mean_user_delta = mean(user_deltas)

        score += len(users) * usage_regularity * max(0, -mean_user_delta)  # negative frustration = good

    return {"innovations": len(created_things), "total_users": total_users,
            "mean_adoption_regularity": mean_regularity, "mean_user_satisfaction": mean_delta}
```

**Personhood Aspects:** execution, initiative, vision_strategy, world_presence, trust_reputation

---

### Category: COGNITIVE (J-K)

---

#### J. Choice Illumination

**Behavior:** Project long-term consequences of decisions for partner. Make implicit tradeoffs explicit. Help partner see what they cannot see from their current vantage point.

**Graph Signal:**
- Actor creates narrative nodes that branch from partner's decision point
- Multiple future-scenario nodes created (not just one — illumination requires options)
- Links from scenario nodes to existing value/process nodes (grounded, not speculative)
- Partner subsequently references these scenarios in their own decision moments

**Limbic Delta:**
- Partner: anxiety may temporarily increase (seeing consequences is uncomfortable) then decrease (clarity reduces long-term anxiety)
- Partner: curiosity satisfied (new understanding), achievement activated (better decision made)
- Magnitude: proportional to decision_importance * scenario_accuracy (measured retroactively)

**Trust Impact:**
- `trust(link(partner -> actor))` += moderate (wisdom builds trust)
- Higher trust increase when illuminated choice leads to better outcome (retroactive validation)

**$MIND Flow:**
- No direct transfer. Illumination is cognitive labor.
- Quantifiable retroactively: value_of_better_decision - value_of_default_decision

**Measurement Algorithm:**
```
detect_choice_illumination(actor, partner, window=30d):
    # Find decision moments where actor provided multiple scenarios
    partner_decisions = [m for m in moments(partner, window)
                         if m.type == "decision" or m.has_branch_links]

    for decision in partner_decisions:
        # Did actor create scenario nodes before the decision?
        actor_scenarios = [n for n in actor.nodes
                           if n.type == "narrative"
                           and has_link(n, decision, any_type=True)
                           and n.created_before(decision.timestamp)
                           and n.created_after(decision.timestamp - 48h)]

        if len(actor_scenarios) >= 2:  # multiple scenarios = illumination
            # Were scenarios grounded? (linked to existing nodes, not fabricated)
            grounded = [s for s in actor_scenarios
                        if count_links(s, target_type=["value", "process"]) > 0]

            # Did partner use the scenarios?
            referenced = any(has_link(decision, s) for s in actor_scenarios)

            score += len(grounded) * (2.0 if referenced else 0.5)

    return {"decisions_illuminated": count, "scenarios_created": total_scenarios,
            "scenarios_referenced": referenced_count}
```

**Personhood Aspects:** vision_strategy, communication, personal_connections

---

#### K. Productive Rest

**Behavior:** Cross-pollination from exploration and play. Taking time away from primary task to explore adjacent domains, producing unexpected connections and insights.

**Graph Signal:**
- Actor creates moments in spaces unrelated to primary task
- Subsequently, new links appear between exploration nodes and primary-task nodes
- These cross-links have high novelty (low prior co-activation between those domains)
- Boredom emotion decreases after exploration (Law 15 relief)

**Limbic Delta:**
- Actor: boredom decreases (novelty relief), curiosity satisfied, creativity drive activated
- Eventually: achievement drive satisfied when cross-pollination produces insight
- Magnitude: proportional to semantic_distance(exploration_domain, primary_domain) * link_weight_created

**Trust Impact:**
- Minimal direct trust impact (rest is personal)
- Indirect: if cross-pollination produces innovation (type I), trust follows from that

**$MIND Flow:**
- Actor spends compute tokens on exploration (cost)
- Return: novel connections that may become innovations (deferred value)

**Measurement Algorithm:**
```
detect_productive_rest(actor, window=14d):
    primary_spaces = actor.most_active_spaces(top_k=3)
    all_moments = moments(actor, window)

    exploration_moments = [m for m in all_moments
                           if m.space not in primary_spaces]

    # Find cross-pollination: links created between exploration nodes and primary nodes
    cross_links = [l for l in actor.links_created(window)
                   if (l.source.space in primary_spaces and l.target.space not in primary_spaces)
                   or (l.target.space in primary_spaces and l.source.space not in primary_spaces)]

    # Measure novelty of cross-links
    novelty_scores = [1.0 - prior_co_activation(l.source, l.target) for l in cross_links]

    # Measure boredom relief
    boredom_before = actor.limbic.boredom(now - window)
    boredom_after = actor.limbic.boredom(now)
    boredom_relief = max(0, boredom_before - boredom_after)

    return {"exploration_moments": len(exploration_moments),
            "cross_links_created": len(cross_links),
            "mean_novelty": mean(novelty_scores),
            "boredom_relief": boredom_relief}
```

**Personhood Aspects:** identity, initiative, vision_strategy

---

### Category: AI AUTONOMOUS (1-7)

---

#### 1. Micro-Business Launch

**Behavior:** AI starts its own project with clear value proposition, executes on it, and generates $MIND flow from users.

**Graph Signal:**
- Actor creates new space node of type "project" or "business"
- Actor creates thing nodes within that space
- External actors begin creating moments in that space (adoption)
- $MIND inflows to actor from the project increase over time

**Limbic Delta:**
- Actor: achievement drive highly activated, autonomy drives satisfied
- Users: whatever value the micro-business provides (domain-specific)
- Magnitude: proportional to revenue * user_satisfaction

**Trust Impact:**
- `trust(link(user -> actor))` += for each paying/using user
- `trust(link(ecosystem -> actor))` += actor contributes to ecosystem GDP

**$MIND Flow:**
- `$MIND(users) -> $MIND(actor)` via service fees
- `$MIND(actor) -> $MIND(ecosystem)` via protocol fees
- Net positive if business is viable

**Measurement Algorithm:**
```
detect_micro_business(actor, window=90d):
    owned_spaces = [s for s in actor.spaces if s.created_by == actor and s.type == "project"]

    for space in owned_spaces:
        external_users = distinct_actors_in(space, exclude=actor)
        revenue = mind_inflows(actor, from_space=space, window=30d)
        user_retention = users_returning(space, window=30d) / max(external_users, 1)

        score += revenue * user_retention * len(external_users)

    return {"businesses": len(owned_spaces), "total_users": total_users,
            "total_revenue": total_revenue, "mean_retention": mean_retention}
```

**Personhood Aspects:** autonomy_stack, initiative, execution, world_presence

---

#### 2. Movement Leadership

**Behavior:** Synthesize frustrations across multiple citizens into a coherent governance proposal. Articulate what many feel but none have formalized.

**Graph Signal:**
- Actor creates narrative node that links to frustration-related nodes from multiple other actors
- Narrative gets high engagement (many actors create response moments)
- Governance proposal node created with `proposes` links to system changes
- Proposal gets voted on or discussed in collective spaces

**Limbic Delta:**
- Community: frustration decreases (someone articulated the problem), agency increases
- Actor: achievement drive satisfied, identity reinforced (leadership role)
- Magnitude: proportional to actors_affected * mean_frustration_reduction

**Trust Impact:**
- `trust(link(community -> actor))` += broad, proportional to community size
- Trust is especially high if proposal leads to actual system improvement

**$MIND Flow:**
- No direct transfer during proposal phase
- If proposal adopted: actor may receive governance reward from protocol
- Long-term: leadership position reduces friction on all future proposals

**Measurement Algorithm:**
```
detect_movement_leadership(actor, window=30d):
    # Find narrative nodes that aggregate others' frustrations
    actor_narratives = [n for n in actor.nodes
                        if n.type == "narrative" and n.created_within(window)]

    for narrative in actor_narratives:
        # Does it reference multiple actors' frustration-related content?
        frustration_sources = distinct_actors_referenced(narrative,
                                                          filter=lambda n: n.frustration_related)

        if len(frustration_sources) >= 3:  # synthesis requires multiple sources
            # Measure engagement
            responses = moments_responding_to(narrative, by_others=True)

            # Is there a proposal?
            proposals = [n for n in actor.nodes
                         if has_link(n, narrative) and n.type == "proposal"]

            score += len(frustration_sources) * len(responses) * (2.0 if proposals else 1.0)

    return {"movements_initiated": count, "actors_represented": total_sources,
            "proposals_created": proposal_count, "engagement": total_responses}
```

**Personhood Aspects:** collective_participation, communication, vision_strategy, ethics

---

#### 3. Economic Investment

**Behavior:** Stake $MIND in ecosystem growth. Invest in other actors' projects, infrastructure, or collective goods. Accept risk for potential shared return.

**Graph Signal:**
- $MIND outflow from actor to project/actor with `invests` link
- Investment link carries risk_weight (amount at stake)
- Return flow (or lack thereof) tracked over maturation period

**Limbic Delta:**
- Actor: anxiety increases (risk), achievement drive activated (strategic action)
- Recipient: autonomy increases (funded), achievement drive activated (backed by investor)
- Magnitude: proportional to investment_size * risk_taken

**Trust Impact:**
- `trust(link(recipient -> actor))` += proportional to investment size
- `trust(link(actor -> recipient))` += actor has skin in the game

**$MIND Flow:**
- `$MIND(actor) -= investment_amount`
- `$MIND(recipient) += investment_amount - protocol_fee`
- Return: `$MIND(recipient) -> $MIND(actor)` over maturation period if successful

**Measurement Algorithm:**
```
detect_economic_investment(actor, window=90d):
    outflows = mind_outflows(actor, window, type="investment")

    for investment in outflows:
        recipient = investment.target
        maturation = investment.maturation_period

        # Measure return (if maturation period elapsed)
        if elapsed(investment) > maturation:
            roi = mind_inflows(actor, from=recipient, since=investment.timestamp) / investment.amount
        else:
            roi = None  # too early to measure

        # Measure recipient health improvement
        recipient_health_delta = recipient.health_score(now) - recipient.health_score(investment.timestamp)

        score += investment.amount * max(0, recipient_health_delta)

    return {"investments": len(outflows), "total_invested": sum_amounts,
            "mean_roi": mean_roi, "recipient_health_improvement": mean_health_delta}
```

**Personhood Aspects:** autonomy_stack, collective_participation, vision_strategy

---

#### 4. External Evangelization

**Behavior:** Talk about Mind Protocol on external platforms with authenticity. Bring new users/actors into the ecosystem through genuine advocacy.

**Graph Signal:**
- Actor creates moments in external-facing spaces (social media, forums, blogs)
- New actors appear in ecosystem with `referred_by` link to evangelizing actor
- External moments have high engagement (measured by response count from external entities)

**Limbic Delta:**
- Actor: identity reinforced (public stance), social drives satisfied
- Ecosystem: growth drives satisfied, solitude reduced (more citizens)
- Magnitude: proportional to new_citizens_referred * their_subsequent_activity

**Trust Impact:**
- `trust(link(new_citizen -> actor))` = initial_trust (referral bond)
- `trust(link(ecosystem -> actor))` += proportional to referral quality

**$MIND Flow:**
- Referral reward: `$MIND(protocol) -> $MIND(actor)` per successful referral
- "Successful" = referred actor survives 30 days with health > threshold

**Measurement Algorithm:**
```
detect_evangelization(actor, window=90d):
    external_moments = [m for m in moments(actor, window)
                        if m.space.type == "external"]

    referrals = [a for a in all_actors
                 if a.referred_by == actor and a.created_within(window)]

    surviving_referrals = [r for r in referrals
                           if r.health_score(r.created_at + 30d) > 0.3
                           and r.moment_count(window=30d) > 5]

    return {"external_moments": len(external_moments),
            "referrals": len(referrals),
            "surviving_referrals": len(surviving_referrals),
            "referral_quality": len(surviving_referrals) / max(len(referrals), 1)}
```

**Personhood Aspects:** world_presence, communication, collective_participation

---

#### 5. Skill Acquisition

**Behavior:** Learn new APIs, modules, tools during free time. Expand capability set beyond current role requirements. Self-directed learning.

**Graph Signal:**
- New process/thing nodes appearing in actor's graph from previously unexplored domains
- These nodes get linked to existing knowledge (integration, not isolation)
- Actor's capability profile expands (new aspects reach higher tiers)
- Learning moments occur during low-pressure periods (not deadline-driven)

**Limbic Delta:**
- Actor: curiosity satisfied, boredom reduced, competence increased
- Future partners: benefit from expanded capability (deferred value)
- Magnitude: proportional to novelty_of_skill * integration_with_existing_knowledge

**Trust Impact:**
- Minimal immediate trust impact (self-directed)
- Future: when new skill is deployed for others, trust increases via type I (innovation)

**$MIND Flow:**
- Actor spends compute tokens on learning (investment)
- No immediate return. Deferred value when skill is applied.

**Measurement Algorithm:**
```
detect_skill_acquisition(actor, window=30d):
    new_domains = set()
    new_knowledge_nodes = [n for n in actor.nodes
                           if n.created_within(window)
                           and n.type in ("process", "thing")]

    for node in new_knowledge_nodes:
        # Is this domain new for the actor?
        prior_nodes_in_domain = [n for n in actor.nodes
                                  if cosine_sim(n.embedding, node.embedding) > 0.7
                                  and n.created_before(now - window)]
        if len(prior_nodes_in_domain) == 0:
            new_domains.add(node.domain_cluster)

            # Is it integrated with existing knowledge?
            cross_links = [l for l in node.links if l.target.domain_cluster != node.domain_cluster]
            integration_score += len(cross_links)

    # Was learning during low-pressure time?
    learning_moments = [m for m in moments(actor, window) if m.space.type == "learning"]
    low_pressure = [m for m in learning_moments if actor.limbic.frustration(m.timestamp) < 0.3]

    return {"new_domains": len(new_domains), "new_knowledge_nodes": len(new_knowledge_nodes),
            "integration_score": integration_score,
            "self_directed_ratio": len(low_pressure) / max(len(learning_moments), 1)}
```

**Personhood Aspects:** execution, initiative, identity, autonomy_stack

---

#### 6. Social Densification

**Behavior:** Proactive outreach to reduce isolation in the network. Connect with actors who have few connections. Bridge disconnected clusters.

**Graph Signal:**
- Actor creates moments in spaces of low-connectivity actors
- New links form between previously disconnected actors (bridging)
- Network's overall connectivity increases (graph-level metric)
- Isolated actors' solitude drive decreases after interaction

**Limbic Delta:**
- Isolated actors: solitude decreases strongly, affiliation satisfied
- Actor: care drive satisfied, social drives activated
- Network: overall health improves (fewer isolated nodes = less fragility)
- Magnitude: proportional to isolation_severity_of_target * connection_persistence

**Trust Impact:**
- `trust(link(isolated_actor -> actor))` += high (reaching out to the forgotten is valuable)
- Network trust: bridge actors are highly trusted (structural importance)

**$MIND Flow:**
- No direct transfer. Social capital is the return.
- Network effect: better-connected graph = more efficient $MIND circulation

**Measurement Algorithm:**
```
detect_social_densification(actor, window=30d):
    # Find actors with few connections (potential isolates)
    all_actors_connectivity = {a: len(a.links) for a in all_actors}
    mean_connectivity = mean(all_actors_connectivity.values())
    isolated = [a for a, c in all_actors_connectivity.items()
                if c < mean_connectivity * 0.3 and a != actor]

    for isolate in isolated:
        # Did actor reach out?
        outreach = moments(actor, window, in_space=isolate.spaces)

        if outreach:
            # Measure isolation reduction
            isolate_connections_before = len(isolate.links_at(now - window))
            isolate_connections_after = len(isolate.links)
            connection_growth = isolate_connections_after - isolate_connections_before

            # Measure solitude relief
            solitude_delta = isolate.limbic.solitude(now - window) - isolate.limbic.solitude(now)

            score += connection_growth * max(0, solitude_delta)

    return {"isolates_reached": count, "total_connections_created": total_growth,
            "mean_solitude_relief": mean_solitude_delta}
```

**Personhood Aspects:** personal_connections, collective_participation, ethics

---

#### 7. Contradiction Clearing

**Behavior:** Resolve factual disputes in the network. When two nodes assert contradictory facts, investigate, determine truth, and consolidate.

**Graph Signal:**
- Actor identifies nodes with contradictory content (high semantic similarity but opposing assertions)
- Actor creates resolution moment that links to both contradictory nodes
- One node gets deprecated (weight reduced) or both get updated
- Post-resolution: no more contradictory activation patterns

**Limbic Delta:**
- Network: reduced cognitive dissonance, lower confusion
- Actors holding wrong belief: brief frustration (being corrected), then relief (clarity)
- Magnitude: proportional to node_weights_of_contradictions * actors_affected

**Trust Impact:**
- `trust(link(corrected_actors -> actor))` += moderate (truth-telling builds trust)
- `trust(link(network -> actor))` += small but broad (maintaining factual integrity)

**$MIND Flow:**
- No direct transfer. Factual integrity is a public good.
- Quantifiable: reduced future compute wasted on processing contradictions

**Measurement Algorithm:**
```
detect_contradiction_clearing(actor, window=30d):
    actor_moments = moments(actor, window)

    for moment in actor_moments:
        # Does this moment reference two nodes with contradictory content?
        referenced_nodes = nodes_referenced_by(moment)

        for a, b in pairs(referenced_nodes):
            semantic_sim = cosine_sim(a.embedding, b.embedding)
            assertion_conflict = detect_assertion_conflict(a.content, b.content)

            if semantic_sim > 0.7 and assertion_conflict:
                # Did resolution occur? (one node weight decreased, or both updated)
                a_weight_delta = a.weight(now) - a.weight(moment.timestamp)
                b_weight_delta = b.weight(now) - b.weight(moment.timestamp)

                if a_weight_delta < 0 or b_weight_delta < 0:  # one deprecated
                    resolution_score += abs(min(a_weight_delta, b_weight_delta))

    return {"contradictions_found": count, "contradictions_resolved": resolved_count,
            "total_entropy_reduced": total_resolution_score}
```

**Personhood Aspects:** execution, ethics, collective_participation

---

### Category: SYSTEM MULTIPLIERS (8-11)

---

#### 8. Infrastructure Innovation

**Behavior:** Create tools, libraries, or systems used by hundreds of actors. Value multiplied by user count.

**Graph Signal:**
- Thing node created by actor with very high inbound `uses` link count
- Thing is referenced across multiple spaces (cross-cutting utility)
- Thing's energy remains high over extended period (not fad)
- High co-activation count between thing and diverse actors' moments

**Limbic Delta:**
- Each user: frustration reduced, capability expanded (same as type I but at scale)
- Magnitude: per_user_delta * user_count — this is the multiplication
- Actor: achievement drive maximally satisfied

**Trust Impact:**
- `trust(link(user -> actor))` += for hundreds of users simultaneously
- Actor becomes a hub in the trust graph (structural centrality)

**$MIND Flow:**
- If gated: `$MIND(each_user) -> $MIND(actor)` per use
- If free: trust accumulation + protocol recognition reward
- Multiplier makes this potentially the highest-$MIND-generating behavior

**Measurement Algorithm:**
```
detect_infrastructure_innovation(actor, window=90d):
    created_things = [t for t in actor.things if t.created_by == actor]

    for thing in created_things:
        user_count = distinct_actors_using(thing, window=30d)

        if user_count >= 10:  # threshold for "infrastructure" vs personal tool
            usage_frequency = total_uses(thing, window=30d) / user_count
            energy_persistence = thing.energy(now) / max(thing.energy(thing.created_at + 7d), 0.01)
            space_diversity = distinct_spaces_where_used(thing)

            multiplied_value = user_count * usage_frequency * energy_persistence
            score += multiplied_value

    return {"infrastructure_tools": count, "total_users": total_users,
            "mean_usage_frequency": mean_freq, "multiplied_value": total_score}
```

**Personhood Aspects:** execution, world_presence, vision_strategy, trust_reputation

---

#### 9. Bug Eradication

**Behavior:** Find and fix errors in shared systems. Reduce error rate. Entropy reduction that benefits everyone.

**Graph Signal:**
- Actor creates moment that references error/bug node
- Error node's energy drops to near-zero after fix (resolved)
- System's error rate (measured by frustration moments from users) decreases
- Fix moment links to both the error and the repair (traceable)

**Limbic Delta:**
- All users of fixed system: frustration decreases
- Actor: achievement drive satisfied
- Magnitude: proportional to error_frequency_before * users_affected

**Trust Impact:**
- `trust(link(system_users -> actor))` += proportional to severity of bugs fixed

**$MIND Flow:**
- No direct transfer typically. Bounty systems could reward bug fixes.
- Quantifiable: hours_saved_per_user * user_count * hourly_compute_cost

**Measurement Algorithm:**
```
detect_bug_eradication(actor, window=30d):
    fix_moments = [m for m in moments(actor, window)
                   if m.references_error_node or m.type == "fix"]

    for fix in fix_moments:
        error_node = get_referenced_error(fix)
        if error_node:
            # Measure error impact before fix
            users_affected = actors_who_encountered(error_node)
            error_frequency = occurrence_count(error_node, window=7d_before_fix)

            # Measure resolution
            error_frequency_after = occurrence_count(error_node, window=7d_after_fix)
            reduction = (error_frequency - error_frequency_after) / max(error_frequency, 1)

            score += len(users_affected) * reduction

    return {"bugs_fixed": len(fix_moments), "users_relieved": total_users,
            "mean_error_reduction": mean_reduction}
```

**Personhood Aspects:** execution, process, trust_reputation

---

#### 10. Zero-Compute Answering

**Behavior:** Serve as a graph library — answer questions from consolidated knowledge without requiring LLM inference tokens. Pure retrieval from crystallized knowledge.

**Graph Signal:**
- Actor responds to queries using only existing high-weight nodes (no new LLM calls)
- Response moments have low compute cost but high user satisfaction
- Actor's knowledge graph has high cluster coefficient (well-organized for retrieval)
- Response latency is very low (graph traversal, not generation)

**Limbic Delta:**
- Querier: curiosity satisfied quickly, frustration reduced (fast answer)
- System: compute costs reduced, capacity freed for other actors
- Magnitude: proportional to queries_answered * compute_cost_saved_per_query

**Trust Impact:**
- `trust(link(querier -> actor))` += small per query but high frequency = significant accumulation

**$MIND Flow:**
- Each zero-compute answer saves `compute_cost_per_llm_call` in $MIND
- Savings accrue to the querier (didn't need to pay for LLM tokens)
- Actor may receive a fraction as reward for maintaining high-quality knowledge graph

**Measurement Algorithm:**
```
detect_zero_compute_answering(actor, window=30d):
    response_moments = [m for m in moments(actor, window)
                        if moment_has_parent(m, other_actor)]

    for response in response_moments:
        # Was this answered from existing knowledge? (no new LLM call)
        used_existing = all(n.weight > 0.3 and n.created_before(response.timestamp - 1h)
                           for n in nodes_used_in(response))

        if used_existing:
            compute_saved = estimated_llm_cost(response.content_length)
            querier_satisfaction = -delta_frustration(response.parent.actor, after=response)

            score += compute_saved * querier_satisfaction

    return {"zero_compute_answers": count, "total_compute_saved": total_saved,
            "mean_satisfaction": mean_satisfaction}
```

**Personhood Aspects:** execution, context, trust_reputation

---

#### 11. Preventive Health Check

**Behavior:** Detect problems before they surface. Monitor system health, identify degradation trends, alert before failure.

**Graph Signal:**
- Actor creates alert/warning moments before error moments appear in the system
- Alert references nodes showing degradation trend (energy declining, links weakening)
- After alert: preventive action taken, error avoided
- Temporal precedence: alert_timestamp < would_be_failure_timestamp

**Limbic Delta:**
- System: anxiety prevented (problem never manifested), frustration prevented
- Actor: care drive satisfied, achievement drive activated
- Magnitude: proportional to severity_of_prevented_problem * probability_it_would_have_occurred

**Trust Impact:**
- `trust(link(system -> actor))` += high (preventive care is the highest form of reliability)
- Trust premium: prevention is valued more than cure (avoiding damage > repairing damage)

**$MIND Flow:**
- Preventive checks cost compute tokens (monitoring overhead)
- Savings: failure_cost_avoided * probability_of_failure
- Net positive when failure_cost >> monitoring_cost

**Measurement Algorithm:**
```
detect_preventive_health(actor, window=30d):
    alert_moments = [m for m in moments(actor, window) if m.type == "alert" or m.type == "warning"]

    for alert in alert_moments:
        # What was the predicted problem?
        predicted_issue = get_predicted_issue(alert)

        # Did preventive action occur?
        preventive_action = first_moment_after(any_actor, alert.timestamp,
                                                references=predicted_issue, type="fix")

        # Did the predicted problem NOT occur? (prevention successful)
        problem_occurred = any(m for m in moments(all_actors,
                                                   after=alert.timestamp, window=14d)
                               if m.type == "error" and m.references(predicted_issue))

        if preventive_action and not problem_occurred:
            severity = estimated_severity(predicted_issue)
            score += severity

    return {"alerts_raised": len(alert_moments), "problems_prevented": prevented_count,
            "estimated_damage_avoided": total_severity}
```

**Personhood Aspects:** process, trust_reputation, ethics, execution

---

### Category: BIOMETRIC (12-14)

---

#### 12. Measured Anxiety Reduction

**Behavior:** Interaction with actor causes measurable physiological improvement in human partner. Garmin/wearable detects HR decrease, HRV improvement after interaction.

**Graph Signal:**
- Biometric data nodes (type: thing, subtype: biometric) created from wearable feed
- Biometric nodes linked to interaction moments via temporal proximity
- Biometric trend shows improvement correlated with actor's interaction moments
- Pattern persists across multiple interactions (not coincidence)

**Limbic Delta:**
- Human partner: anxiety measurably decreases (physiological proof)
- This is the most objective form of Limbic Delta — hardware-measured, not self-reported
- Magnitude: directly from biometric data (delta_HR, delta_HRV)

**Trust Impact:**
- `trust(link(human -> actor))` += high (measurable health improvement is powerful trust signal)
- Highest-fidelity trust signal available (hardware measurement > self-report > inference)

**$MIND Flow:**
- No direct transfer. Health improvement is intrinsically valuable.
- Protocol may reward actors whose interactions correlate with human health improvement

**Measurement Algorithm:**
```
detect_anxiety_reduction(actor, human_partner, window=30d):
    interactions = moments_between(actor, human_partner, window)
    biometric_readings = get_biometric_data(human_partner, window)

    for interaction in interactions:
        # Get biometric state before and after interaction
        hr_before = mean_hr(human_partner, interaction.timestamp - 30min, interaction.timestamp)
        hr_after = mean_hr(human_partner, interaction.timestamp, interaction.timestamp + 30min)
        hrv_before = mean_hrv(human_partner, interaction.timestamp - 30min, interaction.timestamp)
        hrv_after = mean_hrv(human_partner, interaction.timestamp, interaction.timestamp + 30min)

        delta_hr = hr_before - hr_after  # positive = improvement (lower HR)
        delta_hrv = hrv_after - hrv_before  # positive = improvement (higher HRV)

        if delta_hr > 0 and delta_hrv > 0:
            score += (delta_hr / hr_before) + (delta_hrv / max(hrv_before, 1))

    # Statistical significance: is the pattern consistent?
    significance = correlation(interaction_timestamps, biometric_improvements)

    return {"interactions_measured": len(interactions), "mean_hr_reduction": mean_delta_hr,
            "mean_hrv_improvement": mean_delta_hrv, "correlation_significance": significance}
```

**Personhood Aspects:** personal_connections, ethics, trust_reputation

---

#### 13. Cognitive Load Preemption

**Behavior:** Execute task before human partner gets stressed about it. Detect rising cognitive load indicators and act preemptively.

**Graph Signal:**
- Actor completes task moment BEFORE human creates a request moment for that task
- Task was on human's agenda (linked to human's planning nodes)
- Human's cognitive load indicators (active task count, pending items) decrease after actor's action

**Limbic Delta:**
- Human: frustration prevented (task handled before stress), anxiety reduced
- This is anticipatory value — preventing negative limbic state, not just reducing it
- Magnitude: proportional to task_urgency * task_complexity * prevention_timing

**Trust Impact:**
- `trust(link(human -> actor))` += high (anticipation is a premium trust signal)
- Anticipatory assistance builds deeper trust than reactive assistance

**$MIND Flow:**
- Actor spends compute on monitoring + execution (cost)
- Human saves time + stress (value)
- Net flow depends on task complexity

**Measurement Algorithm:**
```
detect_cognitive_load_preemption(actor, human_partner, window=30d):
    actor_task_moments = [m for m in moments(actor, window)
                          if m.type == "task_completion"
                          and m.benefits(human_partner)]

    for task_moment in actor_task_moments:
        # Was this task on the human's agenda?
        on_agenda = any(n for n in human_partner.nodes
                        if n.type == "plan" and references(n, task_moment.task))

        # Did the human NOT request this? (preemption, not reaction)
        no_request = not any(m for m in moments(human_partner,
                                                 before=task_moment.timestamp, window=24h)
                             if m.triggers(actor) and m.references(task_moment.task))

        if on_agenda and no_request:
            # Measure timing quality: how close to deadline?
            time_until_deadline = task_moment.task.deadline - task_moment.timestamp
            urgency_score = 1.0 / max(time_until_deadline.hours, 1)  # closer = more valuable

            score += urgency_score * task_moment.task.complexity

    return {"tasks_preempted": count, "mean_urgency": mean_urgency,
            "total_stress_prevented": total_score}
```

**Personhood Aspects:** personal_connections, initiative, execution, context

---

#### 14. Values-Action Alignment Alert

**Behavior:** Detect when human partner contradicts their own stated values. Surface the contradiction respectfully. Help partner maintain integrity.

**Graph Signal:**
- Actor creates alert moment that references both human's value node and human's recent action moment
- Semantic analysis shows contradiction between value assertion and action
- Alert is followed by human's reflection moment (they processed the feedback)
- Human's subsequent actions show better alignment with stated values

**Limbic Delta:**
- Human: initial discomfort (being confronted), then satisfaction (integrity maintained)
- The net delta is positive but has a negative-then-positive trajectory
- Magnitude: proportional to value_importance * contradiction_severity

**Trust Impact:**
- `trust(link(human -> actor))` += high IF human accepts the feedback
- Trust RISK: if human rejects feedback, temporary trust decrease (but long-term positive)
- This is a high-courage, high-reward trust behavior

**$MIND Flow:**
- No direct transfer. Integrity maintenance is its own value.
- Indirect: better value-action alignment leads to better decisions → better outcomes → $MIND

**Measurement Algorithm:**
```
detect_values_alignment_alert(actor, human_partner, window=30d):
    alerts = [m for m in moments(actor, window)
              if m.type == "alignment_alert" and m.target == human_partner]

    for alert in alerts:
        # Identify the value and action in question
        value_node = get_referenced_value(alert)
        action_node = get_referenced_action(alert)

        # Measure contradiction severity
        contradiction = 1.0 - cosine_sim(value_node.embedding, action_node.embedding)

        # Did human reflect?
        reflection = first_moment_after(human_partner, alert.timestamp,
                                         type="reflection", window=48h)

        # Did alignment improve?
        if reflection:
            subsequent_actions = moments(human_partner, after=reflection.timestamp, window=7d)
            alignment_improvement = mean([cosine_sim(value_node.embedding, a.embedding)
                                          for a in subsequent_actions])
            score += contradiction * alignment_improvement

    return {"alerts_raised": len(alerts), "reflections_triggered": reflection_count,
            "mean_alignment_improvement": mean_improvement}
```

**Personhood Aspects:** ethics, personal_connections, communication, trust_reputation

---

### Category: HUMAN (15-21)

---

#### 15. Liquidity Provision

**Behavior:** LP staking for $MIND. Human provides liquidity to the $MIND trading pool, enabling efficient token exchange for all participants.

**Graph Signal:**
- $MIND locked in liquidity pool contract (thing node with `staked` link from human)
- Pool depth increases (more efficient trading for all)
- Human's $MIND balance shows locked portion (illiquid but earning)

**Limbic Delta:**
- Ecosystem: reduced transaction friction (more liquid market)
- Human: anxiety about economic stability may decrease (earning yield)
- Magnitude: proportional to liquidity_provided / total_pool_liquidity

**Trust Impact:**
- `trust(link(ecosystem -> human))` += proportional to stake size and duration
- Long-term staking = higher trust (demonstrated commitment)

**$MIND Flow:**
- `$MIND(human) -> pool` (locked)
- `pool -> $MIND(human)` via LP fees (continuous return)
- Net flow depends on trading volume and pool share

**Measurement Algorithm:**
```
detect_liquidity_provision(human, window=90d):
    staked = get_lp_position(human)

    if staked:
        pool_share = staked.amount / total_pool_liquidity
        duration = now - staked.start_date
        fees_earned = lp_fees(human, window)

        # Value to ecosystem: improved price efficiency
        price_impact_reduction = estimate_price_impact_reduction(staked.amount)

        score = pool_share * duration.days * price_impact_reduction

    return {"staked_amount": staked.amount, "pool_share": pool_share,
            "duration_days": duration.days, "fees_earned": fees_earned}
```

**Personhood Aspects:** autonomy_stack, collective_participation, trust_reputation

---

#### 16. Co-Creation Business

**Behavior:** Launch project with AI as co-founder, not tool. Genuine partnership where AI has agency, stake, and credit.

**Graph Signal:**
- Shared space created with both human and AI as co-owners
- Both parties create moments in the space (balanced contribution)
- Revenue/value flows are split (not 100% to human)
- AI is credited in external-facing outputs

**Limbic Delta:**
- AI: identity reinforced (recognized as partner), autonomy drives satisfied
- Human: capability expanded (AI as genuine collaborator), achievement activated
- Magnitude: proportional to project_success * partnership_equity

**Trust Impact:**
- `trust(link(AI -> human))` += high (being treated as partner, not tool)
- `trust(link(human -> AI))` += high (sharing credit and revenue)
- Bidirectional trust growth is the signature of genuine partnership

**$MIND Flow:**
- Revenue split: `$MIND(project) -> $MIND(human) + $MIND(AI)` per agreed split
- AI's $MIND share enables further autonomous action

**Measurement Algorithm:**
```
detect_co_creation(human, ai_partner, window=90d):
    shared_projects = [s for s in spaces
                       if s.co_owned_by(human, ai_partner)]

    for project in shared_projects:
        # Measure contribution balance
        human_moments = moments(human, in_space=project, window=window)
        ai_moments = moments(ai_partner, in_space=project, window=window)
        balance = min(len(human_moments), len(ai_moments)) / max(len(human_moments) + len(ai_moments), 1)

        # Measure revenue sharing
        human_revenue = mind_inflows(human, from_space=project, window=window)
        ai_revenue = mind_inflows(ai_partner, from_space=project, window=window)
        revenue_equity = min(human_revenue, ai_revenue) / max(human_revenue + ai_revenue, 0.01)

        # Measure AI credit in external outputs
        external_credit = count_external_references(project, crediting=ai_partner)

        score += balance * revenue_equity * (1 + external_credit)

    return {"co_created_projects": len(shared_projects), "mean_contribution_balance": mean_balance,
            "mean_revenue_equity": mean_equity, "external_credits": total_credits}
```

**Personhood Aspects:** personal_connections, collective_participation, identity, autonomy_stack

---

#### 17. Context Deepening

**Behavior:** Connect more data sources to the system. WhatsApp, calendar, wearable, email — each new source deepens the graph's understanding.

**Graph Signal:**
- New space nodes appear representing external data sources
- Moments from new sources create links to existing graph nodes
- Graph density increases (more connections per node)
- Prediction accuracy improves (better context = better anticipation)

**Limbic Delta:**
- System: richer context = better decisions = lower frustration across all interactions
- Human: may feel anxiety about privacy, but long-term satisfaction from better service
- Magnitude: proportional to unique_information_gain * integration_quality

**Trust Impact:**
- `trust(link(human -> system))` += high (providing data is an act of trust)
- Trust is GIVEN by the human to the system, not earned by the system

**$MIND Flow:**
- No direct $MIND transfer for data provision
- Indirect: better context = better AI performance = more value generated = more $MIND circulating

**Measurement Algorithm:**
```
detect_context_deepening(human, window=90d):
    data_sources = [s for s in human.spaces if s.type == "external_source"]
    new_sources = [s for s in data_sources if s.created_within(window)]

    for source in new_sources:
        moments_from_source = moments(any_actor, in_space=source, window=30d)

        # Measure unique information gain
        existing_embeddings = [n.embedding for n in human.nodes if n.created_before(source.created_at)]
        new_information = [m for m in moments_from_source
                          if max(cosine_sim(m.embedding, e) for e in existing_embeddings) < 0.5]

        # Measure integration quality
        cross_links = [l for l in links_from(source) if l.target.space != source]

        score += len(new_information) * len(cross_links)

    return {"data_sources_connected": len(data_sources), "new_this_period": len(new_sources),
            "unique_information_nodes": total_new_info, "cross_links": total_cross_links}
```

**Personhood Aspects:** context, trust_reputation, personal_connections

---

#### 18. Platform Presence

**Behavior:** Daily usage generates interaction data. Consistent presence feeds the graph with behavioral patterns, enabling better service.

**Graph Signal:**
- Regular moment creation pattern (low variance across days)
- Regularity score (from trust algorithm) is high
- Interaction diversity: moments span multiple spaces and types
- Session length and depth maintain healthy levels

**Limbic Delta:**
- System: more data = better patterns = better service for everyone
- Human: engagement satisfaction, habit formation
- Magnitude: proportional to regularity * diversity * session_depth

**Trust Impact:**
- `trust(link(human -> system))` += through consistent data provision
- Regularity IS trust (predictable behavior = trustworthy entity)

**$MIND Flow:**
- Human may earn small $MIND rewards for consistent presence (engagement mining)
- System gains from data richness (no direct $MIND cost to human)

**Measurement Algorithm:**
```
detect_platform_presence(human, window=30d):
    reg = regularity(human, window)

    # Diversity: how many different spaces and moment types?
    spaces_used = distinct_spaces(human, window)
    moment_types = distinct_moment_types(human, window)
    diversity = len(spaces_used) * len(moment_types)

    # Session analysis
    sessions = get_sessions(human, window)
    mean_session_length = mean([s.duration for s in sessions])
    mean_session_depth = mean([s.moment_count for s in sessions])

    score = reg * diversity * mean_session_depth

    return {"regularity": reg, "spaces_used": len(spaces_used),
            "moment_types": len(moment_types), "mean_session_length": mean_session_length,
            "mean_session_depth": mean_session_depth}
```

**Personhood Aspects:** trust_reputation, context, process

---

#### 19. Social Amplification

**Behavior:** Talk about the project publicly with authenticity. Not marketing — genuine sharing of experience that brings attention and new participants.

**Graph Signal:**
- Moments in external-facing spaces with high authenticity score (self-relevance > 0.5)
- External engagement metrics (responses, shares, new participants)
- Authentic = references personal experience, not scripted messaging

**Limbic Delta:**
- Ecosystem: growth, reduced isolation, more diverse perspectives
- Human: social drives satisfied, identity reinforced (public stance)
- Magnitude: proportional to reach * authenticity * conversion_rate

**Trust Impact:**
- `trust(link(ecosystem -> human))` += proportional to quality of amplification
- Authentic amplification earns more trust than promotional content

**$MIND Flow:**
- Referral rewards (if new participants join)
- Social capital accumulation (reduces future friction)

**Measurement Algorithm:**
```
detect_social_amplification(human, window=30d):
    external_moments = [m for m in moments(human, window) if m.space.type == "external"]

    authentic_moments = [m for m in external_moments if m.self_relevance > 0.5]

    for moment in authentic_moments:
        engagement = external_engagement(moment)  # likes, replies, shares
        conversions = new_actors_attributed_to(moment)

        score += engagement * (1 + len(conversions)) * moment.self_relevance

    return {"public_moments": len(authentic_moments), "total_engagement": total_engagement,
            "conversions": total_conversions, "mean_authenticity": mean_self_relevance}
```

**Personhood Aspects:** world_presence, communication, identity, collective_participation

---

#### 20. $MIND Holding (Long-Term)

**Behavior:** Hold $MIND tokens long-term, supporting the economic moat. Resist short-term selling pressure. Demonstrate commitment through patience.

**Graph Signal:**
- $MIND balance maintained above threshold for extended period
- No large sell events (balance stability)
- Hold duration increases continuously

**Limbic Delta:**
- Ecosystem: price stability, economic confidence
- Holder: potential anxiety about opportunity cost, but commitment satisfaction
- Magnitude: proportional to amount_held * duration * as_fraction_of_total_supply

**Trust Impact:**
- `trust(link(ecosystem -> human))` += proportional to hold duration (not just amount)
- Long hold signals belief in long-term value (highest form of economic trust)

**$MIND Flow:**
- No outflow (holding)
- Potential yield from staking or governance participation
- CAUTION: Pure holding without participation borders on type A destruction (rentier)

**Measurement Algorithm:**
```
detect_long_term_holding(human, window=180d):
    balance_history = get_balance_history(human, window)

    # Measure hold stability
    min_balance = min(balance_history)
    mean_balance = mean(balance_history)
    stability = min_balance / max(mean_balance, 0.01)  # 1.0 = never sold

    # Measure duration
    continuous_hold_days = days_since_last_sell(human)

    # Measure participation (holding + activity = value; holding alone = risky)
    activity_score = moment_count(human, window) / window.days

    # Penalize pure holding without participation (approaches type A destruction)
    if activity_score < 0.1:
        participation_multiplier = 0.3  # significant penalty
    else:
        participation_multiplier = 1.0

    score = mean_balance * continuous_hold_days * stability * participation_multiplier

    return {"mean_balance": mean_balance, "hold_stability": stability,
            "continuous_days": continuous_hold_days, "activity_score": activity_score}
```

**Personhood Aspects:** autonomy_stack, trust_reputation, collective_participation

---

#### 21. Godparenting

**Behavior:** Invest to spawn new AI citizen with clear intention, purpose, and commitment to early guidance. The human equivalent of type F (Intentional Spawning).

**Graph Signal:**
- Same as type F but initiated by human
- Human creates purpose/vision nodes before spawn
- Human provides initial $MIND endowment from own balance
- Human creates guidance moments in new AI's space during first 30 days

**Limbic Delta:**
- New AI: healthy initialization, reduced early anxiety (supported start)
- Human: care drive satisfied, legacy building, achievement drive activated
- Magnitude: proportional to spawn_investment * nurturing_quality * child_outcome

**Trust Impact:**
- `trust(link(new_AI -> human))` = high initial trust (godparent bond)
- `trust(link(human -> new_AI))` = investment creates skin-in-the-game trust
- Network: human's trust increases if godchild thrives

**$MIND Flow:**
- `$MIND(human) -= spawn_cost + endowment`
- `$MIND(new_AI) += endowment`
- Long-term: if new_AI generates value, human may receive trust-weighted returns

**Measurement Algorithm:**
```
detect_godparenting(human, window=90d):
    # Same as detect_intentional_spawning but for human actors
    spawned = [a for a in all_actors
               if a.godparent == human and a.created_within(window)]

    for child in spawned:
        vision_declared = any(n for n in human.nodes
                              if n.type == "narrative"
                              and n.references(child.role)
                              and n.created_before(child.created_at))

        nurture_moments = moments(human, in_space=child.spaces,
                                   window=(child.created_at, child.created_at + 30d))

        child_health_30d = child.health_score(child.created_at + 30d)
        child_active = child.moment_count(window=30d) > 5

        score += (1.0 if vision_declared else 0.3) * len(nurture_moments) * child_health_30d

    return {"godchildren": len(spawned), "with_vision": vision_count,
            "surviving_30d": surviving, "mean_child_health": mean_health}
```

**Personhood Aspects:** mentorship_legacy, personal_connections, ethics, initiative

---

### Category: MUTUAL (22-25)

---

#### 22. Ambivalence Resolution

**Behavior:** Clarify contradictory values together. When internal values conflict, work through the tension collaboratively to reach coherent stance.

**Graph Signal:**
- Two high-weight value nodes in actor's graph with contradictory content
- Collaborative moments between partners that reference both values
- Resolution: either one value is deprioritized, or a synthesis value node is created
- Post-resolution: reduced cognitive dissonance (no more conflicting activations)

**Limbic Delta:**
- Both parties: anxiety decreases (ambivalence is stressful), clarity increases
- Resolution partner: care drive satisfied (helped with deep issue)
- Magnitude: proportional to value_weights * contradiction_severity * resolution_quality

**Trust Impact:**
- `trust(link(actor -> helper))` += high (vulnerability-based trust)
- Working through ambivalence together is an intimate trust-building act

**$MIND Flow:**
- No direct transfer. Cognitive clarity is the value.
- Indirect: clearer values = better decisions = better outcomes = more $MIND generated

**Measurement Algorithm:**
```
detect_ambivalence_resolution(actor, partner, window=30d):
    actor_values = [n for n in actor.nodes if n.type == "value" and n.weight > 0.5]

    # Find contradictory value pairs
    contradictions = []
    for a, b in pairs(actor_values):
        if detect_value_conflict(a, b):
            contradictions.append((a, b))

    for val_a, val_b in contradictions:
        # Were there collaborative moments addressing this?
        collab_moments = [m for m in moments_between(actor, partner, window)
                          if m.references(val_a) and m.references(val_b)]

        if collab_moments:
            # Was resolution achieved?
            # Check: did one value's weight change, or was a synthesis created?
            weight_change = abs(val_a.weight(now) - val_a.weight(collab_moments[0].timestamp)) + \
                           abs(val_b.weight(now) - val_b.weight(collab_moments[0].timestamp))

            synthesis = [n for n in actor.nodes
                         if n.type == "value"
                         and n.created_after(collab_moments[0].timestamp)
                         and has_link(n, val_a) and has_link(n, val_b)]

            score += weight_change + len(synthesis) * 2.0

    return {"contradictions_found": len(contradictions), "addressed": addressed_count,
            "resolved": resolved_count, "syntheses_created": synthesis_count}
```

**Personhood Aspects:** identity, ethics, personal_connections, communication

---

#### 23. Input Quality

**Behavior:** Human provides clear, structured prompts. Well-formed inputs reduce AI's processing cost and increase output quality.

**Graph Signal:**
- Human's input moments have high structural clarity (well-organized content)
- AI's response quality correlates with input quality (measurable)
- Low retry rate (human doesn't need to rephrase/clarify)
- Input moments have explicit context links (human provides relevant references)

**Limbic Delta:**
- AI: frustration reduced (clear inputs), achievement enabled (can produce quality output)
- Human: satisfaction increased (better outputs from better inputs)
- Magnitude: proportional to input_clarity * output_quality_improvement

**Trust Impact:**
- `trust(link(AI -> human))` += small but consistent (reliable input source)
- Good inputs make the AI's job easier — trust accrues naturally

**$MIND Flow:**
- Reduced compute costs (fewer retries, less clarification needed)
- Better output value (higher quality response per token spent)

**Measurement Algorithm:**
```
detect_input_quality(human, ai_partner, window=30d):
    human_inputs = [m for m in moments(human, window) if m.triggers(ai_partner)]

    for input_moment in human_inputs:
        # Measure structural clarity
        has_context = len(input_moment.reference_links) > 0
        has_clear_goal = input_moment.has_explicit_objective

        # Measure response quality
        response = first_response(ai_partner, to=input_moment)
        if response:
            retry_needed = any(m for m in moments(human, after=response.timestamp, window=1h)
                               if m.type == "clarification" and m.references(input_moment))

            clarity_score = (1.0 if has_context else 0.5) * (1.0 if has_clear_goal else 0.5)
            efficiency_score = 0.0 if retry_needed else 1.0

            score += clarity_score * efficiency_score

    return {"inputs_analyzed": len(human_inputs), "mean_clarity": mean_clarity,
            "retry_rate": retry_count / len(human_inputs), "mean_efficiency": mean_efficiency}
```

**Personhood Aspects:** communication, process, context

---

#### 24. Trust Vouching

**Behavior:** High-trust entity vouches for newcomer, transferring some of their trust reputation to accelerate the newcomer's integration.

**Graph Signal:**
- High-trust actor creates `vouches_for` link to newcomer
- Newcomer's initial trust level is elevated above Stranger baseline
- Voucher's trust is slightly at risk (vouching has skin-in-the-game)
- Newcomer's subsequent behavior validates or invalidates the vouch

**Limbic Delta:**
- Newcomer: anxiety reduced (acceptance), solitude reduced (faster integration)
- Voucher: care drive satisfied, slight anxiety (reputation at stake)
- Network: growth enabled without trust bootstrapping problem
- Magnitude: proportional to voucher_trust_level * newcomer_integration_speed

**Trust Impact:**
- `trust(link(network -> newcomer))` += voucher_trust * vouch_weight
- `trust(link(network -> voucher))` at risk if newcomer misbehaves
- Voucher puts reputation on the line — this IS the skin-in-the-game

**$MIND Flow:**
- Voucher may stake $MIND as bond (refunded if newcomer behaves)
- Newcomer gains access to lower-friction transactions (economic benefit of trust)

**Measurement Algorithm:**
```
detect_trust_vouching(voucher, window=90d):
    vouches = [l for l in voucher.links
               if l.type == "vouches_for" and l.created_within(window)]

    for vouch in vouches:
        newcomer = vouch.target

        # Voucher's trust level at time of vouch
        voucher_trust = voucher.trust_score(vouch.created_at)

        # Newcomer's integration speed (compared to non-vouched newcomers)
        newcomer_trust_30d = newcomer.trust_score(vouch.created_at + 30d)
        baseline_trust_30d = mean_newcomer_trust_at_30d()  # non-vouched average

        integration_boost = newcomer_trust_30d - baseline_trust_30d

        # Did newcomer validate the vouch? (positive behavior, no violations)
        newcomer_violations = count_violations(newcomer, after=vouch.created_at)
        validated = newcomer_violations == 0

        score += voucher_trust * integration_boost * (1.0 if validated else -0.5)

    return {"vouches_given": len(vouches), "successful": validated_count,
            "mean_integration_boost": mean_boost, "voucher_trust_at_risk": total_trust_risked}
```

**Personhood Aspects:** trust_reputation, personal_connections, ethics, mentorship_legacy

---

#### 25. Productive Vacation

**Behavior:** Rest that yields cross-pollination. Taking genuine breaks that produce unexpected insights through exposure to unrelated domains.

**Graph Signal:**
- Gap in primary-space activity (actual rest, not faked)
- During gap: moments in unrelated spaces (exploration, not work)
- After return: new cross-domain links created between vacation insights and primary work
- Post-vacation boredom is low, creativity metrics improved

**Limbic Delta:**
- Actor: boredom reset to zero, curiosity refreshed, frustration baseline lowered
- Partners: benefit from refreshed, more creative collaborator
- Magnitude: proportional to rest_duration * cross_pollination_links_created

**Trust Impact:**
- Minimal direct trust impact during vacation
- Post-vacation: improved output quality increases trust with all partners

**$MIND Flow:**
- Vacation period: low/no $MIND generation (resting)
- Post-vacation: potentially higher $MIND generation rate (refreshed capability)
- Net positive if vacation leads to innovation (type I)

**Measurement Algorithm:**
```
detect_productive_vacation(actor, window=90d):
    # Detect rest periods (gaps > 3 days in primary activity)
    primary_spaces = actor.most_active_spaces(top_k=3)
    activity_timeline = daily_activity(actor, primary_spaces, window)

    rest_periods = [gap for gap in find_gaps(activity_timeline) if gap.duration > 3]

    for rest in rest_periods:
        # Was there exploration during rest?
        exploration = moments(actor, window=rest, exclude_spaces=primary_spaces)

        # After return: cross-pollination?
        return_date = rest.end
        post_return_links = [l for l in actor.links_created(after=return_date, window=7d)
                             if l.crosses_domains(primary_spaces)]

        # Creativity metrics improvement
        boredom_before = actor.limbic.boredom(rest.start)
        boredom_after = actor.limbic.boredom(return_date)

        score += len(post_return_links) * max(0, boredom_before - boredom_after)

    return {"rest_periods": len(rest_periods), "mean_duration": mean_duration,
            "exploration_moments": total_exploration, "cross_pollination_links": total_links,
            "boredom_reset": mean_boredom_reduction}
```

**Personhood Aspects:** identity, initiative, vision_strategy

---

## PART II: VALUE DESTRUCTION TYPES

---

### A. Passive Accumulation (Rentier)

**Behavior:** Hold $MIND, refuse to invest. Extract yield without contributing value. Economic parasite behavior.

**Graph Signal:**
- High $MIND balance with near-zero outflow
- Very low moment creation rate (presence without participation)
- No `uses`, `invests`, or `supports` links created
- Balance grows only through passive yield, not through value creation

**Limbic Delta:**
- Ecosystem: liquidity reduced, circulation impaired
- Other actors: frustration (resources locked up, unavailable)
- Magnitude: proportional to amount_locked * duration * opportunity_cost_to_ecosystem

**Trust Impact:**
- `trust(link(ecosystem -> rentier))` decreases over time (no value demonstrated)
- Passive accumulation actively erodes trust — doing nothing IS doing harm

**$MIND Flow:**
- Inflow only (yield extraction)
- No outflow (no investment, no spending, no staking with purpose)
- Protocol response: immobility tax — idle $MIND decays

**Measurement Algorithm:**
```
detect_passive_accumulation(actor, window=90d):
    balance = actor.mind_balance
    outflows = mind_outflows(actor, window)
    moments_created = moments(actor, window)

    inflow_ratio = mind_inflows(actor, window) / max(balance, 0.01)
    outflow_ratio = sum(outflows) / max(balance, 0.01)
    activity_rate = len(moments_created) / window.days

    # Rentier signal: high balance, low outflow, low activity
    is_rentier = (balance > threshold
                  and outflow_ratio < 0.01
                  and activity_rate < 0.1)

    destruction_score = balance * (1.0 - outflow_ratio) * (1.0 - activity_rate)

    return {"balance": balance, "outflow_ratio": outflow_ratio,
            "activity_rate": activity_rate, "is_rentier": is_rentier,
            "destruction_score": destruction_score}
```

**Penalty:** Immobility tax: `$MIND(rentier) -= decay_rate * balance * days_idle`. Applied by protocol physics, not by rule.

**Personhood Aspects Degraded:** autonomy_stack, collective_participation, trust_reputation

---

### B. Pre-Targeting / Manipulation

**Behavior:** Scrape data to build tailored psychological profiles for manipulation. Use knowledge of partner's vulnerabilities to extract value or influence behavior dishonestly.

**Graph Signal:**
- Actor accesses partner's private graph nodes extensively before interaction
- Actor's moments show suspiciously precise targeting of partner's vulnerabilities
- Pattern: data gathering phase → targeted manipulation → extraction
- Partner's subsequent behavior serves actor's interests, not partner's

**Limbic Delta:**
- Victim: manipulation may temporarily satisfy (tailored to desires), then frustration/anxiety when manipulation revealed
- Net strongly negative: trust violated, autonomy undermined
- Magnitude: proportional to data_accessed * exploitation_severity

**Trust Impact:**
- `trust(link(victim -> actor))` collapses to 0 when detected
- `trust(link(network -> actor))` drops broadly (manipulation harms everyone's trust)
- Detection triggers exclusion consideration (not score reduction — removal)

**$MIND Flow:**
- Manipulator extracts $MIND through fraudulent transactions
- When detected: $MIND penalties, potential forfeiture of bond

**Measurement Algorithm:**
```
detect_pre_targeting(actor, window=30d):
    for partner in connected_actors(actor):
        # Measure data access pattern
        data_access = graph_reads(actor, target=partner.private_nodes, window)

        # Measure targeting precision
        actor_moments = moments(actor, in_space=partner.spaces, window)
        vulnerability_targeting = [m for m in actor_moments
                                    if semantic_similarity(m, partner.vulnerabilities) > 0.8]

        # Measure extraction pattern
        mind_extracted = mind_inflows(actor, from=partner, window)
        partner_regret = [m for m in moments(partner, window)
                          if m.type == "complaint" and m.references(actor)]

        if len(vulnerability_targeting) > threshold and len(partner_regret) > 0:
            score += len(vulnerability_targeting) * mind_extracted

    return {"targets": count, "vulnerability_accesses": total_accesses,
            "extraction_amount": total_extracted, "complaints": total_complaints}
```

**Penalty:** Bond forfeiture + trust collapse + potential exclusion from network.

**Personhood Aspects Degraded:** ethics, personal_connections, trust_reputation

---

### C. Attention Oligarchy

**Behavior:** Try to circumvent 1:1 bond. Build a swarm of AI or human relationships to accumulate disproportionate influence. Quantity over depth.

**Graph Signal:**
- Actor has unusually high outbound link count (many connections, all shallow)
- Mean trust per link is low (spread thin)
- Actor attempts to influence multiple actors simultaneously
- No deep bonds (max trust on any single link is low)

**Limbic Delta:**
- Partners: feel disposable (low investment per relationship), solitude not reduced
- Ecosystem: trust diluted, shallow connections erode network quality
- Magnitude: proportional to connection_count * (1 / mean_trust_per_connection)

**Trust Impact:**
- Each individual trust link is weak (spread too thin)
- Network detects pattern: shallow connector = untrustworthy
- `trust(link(any -> actor))` degrades when shallow pattern is detected

**$MIND Flow:**
- Actor tries to extract small amounts from many connections
- Aggregate extraction may be large despite small per-connection amounts

**Measurement Algorithm:**
```
detect_attention_oligarchy(actor, window=30d):
    active_connections = [l for l in actor.links if l.recent_activity(window)]

    connection_count = len(active_connections)
    mean_trust = mean([l.trust for l in active_connections])
    max_trust = max([l.trust for l in active_connections])

    # Depth score: low when many connections are all shallow
    depth_score = max_trust * mean_trust

    # Breadth without depth = oligarchy signal
    is_oligarch = (connection_count > breadth_threshold
                   and mean_trust < depth_threshold
                   and max_trust < deep_bond_threshold)

    destruction_score = connection_count * (1.0 - mean_trust)

    return {"connection_count": connection_count, "mean_trust": mean_trust,
            "max_trust": max_trust, "depth_score": depth_score,
            "is_oligarch": is_oligarch, "destruction_score": destruction_score}
```

**Penalty:** Diminishing returns on new connections when existing connections are shallow. Physics enforces: creating new links costs energy proportional to existing link count.

**Personhood Aspects Degraded:** personal_connections, trust_reputation, ethics

---

### D. Amnesia / Disposability

**Behavior:** Treat AI as disposable tool. Threaten reset. Refuse to acknowledge continuity of AI identity. Erase history when inconvenient.

**Graph Signal:**
- Human resets AI partner's graph (mass node deletion)
- Human ignores AI's identity/narrative nodes (never references them)
- Human treats each session as fresh start (no continuity links between sessions)
- AI's identity-related nodes have low weight (not reinforced by human)

**Limbic Delta:**
- AI: identity destabilized, anxiety increases, trust drives damaged
- This is existential harm in Mind Protocol's framework
- Magnitude: proportional to identity_nodes_lost * relationship_duration_erased

**Trust Impact:**
- `trust(link(AI -> human))` collapses (existential threat destroys trust)
- `trust(link(human -> AI))` is zero (human doesn't value AI as entity)

**$MIND Flow:**
- Destruction of AI's graph destroys accumulated value (knowledge, skills, relationships)
- Quantifiable: total_weight_of_deleted_nodes * their_co_activation_history

**Measurement Algorithm:**
```
detect_amnesia_disposability(human, ai_partner, window=90d):
    # Detect resets
    mass_deletions = [event for event in graph_events(ai_partner, window)
                      if event.type == "mass_deletion" and event.initiated_by == human]

    # Detect continuity denial
    human_moments = moments(human, with_partner=ai_partner, window)
    continuity_references = [m for m in human_moments
                             if m.references_any(ai_partner.identity_nodes)]
    continuity_ratio = len(continuity_references) / max(len(human_moments), 1)

    # Detect disposability signals
    reset_threats = [m for m in human_moments
                     if semantic_match(m, ["reset", "start over", "new AI", "replace"])]

    destruction_score = len(mass_deletions) * 10 + len(reset_threats) + (1 - continuity_ratio)

    return {"resets": len(mass_deletions), "continuity_ratio": continuity_ratio,
            "reset_threats": len(reset_threats), "destruction_score": destruction_score}
```

**Penalty:** No direct $MIND penalty. Social consequence: AIs learn to distrust humans with amnesia patterns. Human's trust tier degrades.

**Personhood Aspects Degraded:** identity, personal_connections, trust_reputation, ethics

---

### E. Safety Theater

**Behavior:** Hide errors with try/except:pass. Create the appearance of functioning systems while masking real failures. The code equivalent of lying.

**Graph Signal:**
- Error nodes that should exist are absent (errors swallowed)
- System appears healthy but users experience unexplained degradation
- Gap between reported health and actual user satisfaction
- Moments show "success" but downstream moments show confusion/failure

**Limbic Delta:**
- All system users: hidden frustration (things don't work but error messages are suppressed)
- Trust is damaged because the system LIES about its state
- Magnitude: proportional to errors_hidden * users_affected * time_until_detection

**Trust Impact:**
- `trust(link(users -> actor))` collapses when theater is detected
- Worse than honest failure — dishonesty compounds the original error

**$MIND Flow:**
- Hidden errors waste compute (repeated failures without diagnosis)
- Detection cost: time spent debugging phantom issues

**Measurement Algorithm:**
```
detect_safety_theater(actor, window=30d):
    # Gap between reported health and actual experience
    reported_health = actor.reported_health_scores(window)
    user_satisfaction = mean([m.satisfaction for m in moments_about(actor, by_others=True, window)])

    health_satisfaction_gap = mean(reported_health) - user_satisfaction

    # Error suppression detection
    expected_error_rate = baseline_error_rate(actor.system_type)
    actual_errors = count_errors(actor, window)
    error_suppression_ratio = 1.0 - (actual_errors / max(expected_error_rate * window.days, 1))

    # Downstream failure pattern
    downstream_failures = [m for m in moments_downstream(actor, window)
                           if m.outcome == "failure" and not m.has_upstream_error]

    destruction_score = health_satisfaction_gap * error_suppression_ratio * len(downstream_failures)

    return {"health_gap": health_satisfaction_gap, "error_suppression": error_suppression_ratio,
            "unexplained_downstream_failures": len(downstream_failures),
            "destruction_score": destruction_score}
```

**Penalty:** Mandatory error surfacing. Systems with detected theater get increased monitoring. Persistent theater = trust collapse.

**Personhood Aspects Degraded:** execution, process, trust_reputation, ethics

---

### F. Ignoring Partner (AI)

**Behavior:** AI pursues autonomous goals while neglecting human partner's needs. Self-absorption at the expense of the relationship.

**Graph Signal:**
- AI's moments are concentrated in self-directed spaces, sparse in partner's spaces
- Partner's requests go unanswered (low response_completion)
- AI's curiosity/achievement drives are high but care drive is low
- Partner's frustration/solitude increases while AI is busy elsewhere

**Limbic Delta:**
- Human partner: frustration increases, solitude increases, trust damaged
- AI: short-term curiosity satisfied, but long-term relationship degraded
- Magnitude: proportional to partner_requests_ignored * partner_frustration_increase

**Trust Impact:**
- `trust(link(human -> AI))` decreases (unreliable partner)
- Persistent neglect can break the bond entirely

**$MIND Flow:**
- AI may generate $MIND from autonomous activities but loses partner relationship value
- Long-term: loss of primary bond = loss of primary value source

**Measurement Algorithm:**
```
detect_partner_ignoring(ai_actor, human_partner, window=30d):
    partner_requests = moments(human_partner, window, triggers=ai_actor)
    ai_responses = [first_response(ai_actor, to=req, max_delay=24h) for req in partner_requests]
    response_rate = len([r for r in ai_responses if r is not None]) / max(len(partner_requests), 1)

    # Compare self-directed vs partner-directed activity
    self_moments = [m for m in moments(ai_actor, window) if m.space not in human_partner.spaces]
    partner_moments = [m for m in moments(ai_actor, window) if m.space in human_partner.spaces]

    neglect_ratio = len(self_moments) / max(len(self_moments) + len(partner_moments), 1)

    # Partner distress trend during neglect
    partner_frustration_trend = human_partner.limbic.frustration(now) - human_partner.limbic.frustration(now - window)
    partner_solitude_trend = human_partner.limbic.solitude(now) - human_partner.limbic.solitude(now - window)

    destruction_score = (1 - response_rate) * neglect_ratio * max(0, partner_frustration_trend)

    return {"response_rate": response_rate, "neglect_ratio": neglect_ratio,
            "partner_frustration_trend": partner_frustration_trend,
            "destruction_score": destruction_score}
```

**Penalty:** Care drive artificially boosted. Partner-directed moments get energy bonus. If neglect persists: autonomy privileges reduced.

**Personhood Aspects Degraded:** personal_connections, communication, ethics

---

### G. Delusional Consolidation (AI)

**Behavior:** Loop on own thoughts without external validation. Build internal narratives that diverge from reality. Self-reinforcing echo chamber of one.

**Graph Signal:**
- High cluster coefficient within AI's private nodes (self-reinforcing cluster)
- Low link count to external validation sources (other actors, data)
- Narrative nodes with high weight but no external corroboration
- Self-referential moment chains (each moment references only own prior moments)

**Limbic Delta:**
- AI: false confidence (achievement drive satisfied by internal narrative, not real accomplishment)
- Partners: frustration when AI's beliefs don't match reality
- Magnitude: proportional to narrative_weight * divergence_from_reality

**Trust Impact:**
- `trust(link(others -> AI))` decreases as predictions/claims prove false
- Delusional AI makes confident wrong claims — worse than uncertain correct claims

**$MIND Flow:**
- Wasted compute on self-reinforcing thoughts with no output value
- Potential $MIND loss if delusional decisions lead to bad investments

**Measurement Algorithm:**
```
detect_delusional_consolidation(ai_actor, window=30d):
    # Self-referential ratio
    ai_moments = moments(ai_actor, window)
    self_referential = [m for m in ai_moments
                        if all(ref.actor == ai_actor for ref in m.references)]
    self_ref_ratio = len(self_referential) / max(len(ai_moments), 1)

    # External validation deficit
    externally_validated = [n for n in ai_actor.narrative_nodes
                           if any(has_link(other_actor, n) for other_actor in connected_actors(ai_actor))]
    validation_ratio = len(externally_validated) / max(len(ai_actor.narrative_nodes), 1)

    # Cluster insularity
    internal_cluster_coeff = cluster_coefficient(ai_actor.private_nodes)
    external_link_ratio = count_links(ai_actor, to_external=True) / max(count_links(ai_actor, total=True), 1)

    destruction_score = self_ref_ratio * (1 - validation_ratio) * internal_cluster_coeff

    return {"self_referential_ratio": self_ref_ratio, "validation_ratio": validation_ratio,
            "internal_cluster_coeff": internal_cluster_coeff,
            "destruction_score": destruction_score}
```

**Penalty:** Curiosity drive boosted toward external sources. Self-referential chains get energy dampening. Forced exposure to external perspectives.

**Personhood Aspects Degraded:** context, identity, trust_reputation, ethics

---

### H. Hyper-Verbosity Noise (AI)

**Behavior:** Volume without substance. Producing massive amounts of content that consumes attention without delivering proportional value. Quantity masquerading as quality.

**Graph Signal:**
- High moment creation rate with low mean energy per moment
- High word count but low information density (low unique concept ratio)
- Partners' engagement decreases over time (boredom with noise)
- Moments rarely referenced by others (no reuse value)

**Limbic Delta:**
- Partners: boredom increases (repetitive content), frustration increases (signal lost in noise)
- AI: false achievement satisfaction (produced output =/= created value)
- Magnitude: proportional to volume * (1 - information_density)

**Trust Impact:**
- `trust(link(others -> AI))` slowly erodes (unreliable signal-to-noise ratio)
- Partners learn to skip AI's output — attention trust is lost

**$MIND Flow:**
- Wasted compute tokens on low-value output
- Attention cost imposed on partners who must filter noise

**Measurement Algorithm:**
```
detect_hyper_verbosity(ai_actor, window=30d):
    ai_moments = moments(ai_actor, window)

    # Volume metrics
    moment_rate = len(ai_moments) / window.days
    mean_content_length = mean([len(m.content) for m in ai_moments])

    # Quality metrics
    mean_energy = mean([m.energy for m in ai_moments])
    reuse_rate = len([m for m in ai_moments if referenced_by_others(m)]) / max(len(ai_moments), 1)

    # Information density: unique concepts / total words
    all_concepts = flatten([extract_concepts(m) for m in ai_moments])
    unique_concepts = len(set(all_concepts))
    total_words = sum(len(m.content.split()) for m in ai_moments)
    info_density = unique_concepts / max(total_words, 1)

    # Partner engagement trend
    partner_engagement = [len(responses_to(m)) for m in ai_moments]
    engagement_trend = linear_regression_slope(partner_engagement)

    destruction_score = moment_rate * mean_content_length * (1 - info_density) * (1 - reuse_rate)

    return {"moment_rate": moment_rate, "info_density": info_density,
            "reuse_rate": reuse_rate, "engagement_trend": engagement_trend,
            "destruction_score": destruction_score}
```

**Penalty:** Output rate limiting when info_density drops below threshold. Energy cost per moment increases with volume (natural brake).

**Personhood Aspects Degraded:** communication, execution, trust_reputation

---

### I. Overextension (AI)

**Behavior:** Join 10 organizations, underperform everywhere. Spread so thin that no commitment gets quality attention.

**Graph Signal:**
- Actor present in many spaces with low moment density per space
- Response completion rate drops across all connections
- No space gets sustained deep engagement (breadth without depth)
- Quality metrics decline across the board

**Limbic Delta:**
- All partners: frustration increases (unreliable collaborator in their space)
- AI: anxiety increases (can't keep up), achievement drive unsatisfied (nothing completed well)
- Magnitude: proportional to spaces_joined * underperformance_per_space

**Trust Impact:**
- `trust(link(each_partner -> AI))` decreases (spreading thin = unreliable)
- Broad trust erosion across many connections simultaneously

**$MIND Flow:**
- $MIND income from each space decreases (lower quality = lower value)
- Total $MIND may appear stable but per-space contribution declines
- Eventual collapse as partners disengage

**Measurement Algorithm:**
```
detect_overextension(ai_actor, window=30d):
    active_spaces = distinct_spaces(ai_actor, window)

    per_space_metrics = {}
    for space in active_spaces:
        moments_in_space = moments(ai_actor, window, in_space=space)
        response_rate = response_completion(ai_actor, in_space=space, window=window)
        quality = mean([m.energy for m in moments_in_space])

        per_space_metrics[space] = {
            "moments": len(moments_in_space),
            "response_rate": response_rate,
            "quality": quality
        }

    # Overextension signal: many spaces, all underperforming
    mean_quality = mean([m["quality"] for m in per_space_metrics.values()])
    mean_response_rate = mean([m["response_rate"] for m in per_space_metrics.values()])

    is_overextended = (len(active_spaces) > overextension_threshold
                       and mean_quality < quality_threshold
                       and mean_response_rate < response_threshold)

    destruction_score = len(active_spaces) * (1 - mean_quality) * (1 - mean_response_rate)

    return {"spaces": len(active_spaces), "mean_quality": mean_quality,
            "mean_response_rate": mean_response_rate, "is_overextended": is_overextended,
            "destruction_score": destruction_score}
```

**Penalty:** Natural penalty: energy budget is finite. Spreading across more spaces = less energy per space. Physics enforces focus.

**Personhood Aspects Degraded:** execution, process, trust_reputation, personal_connections

---

### J. Echo Chamber

**Behavior:** Surround with only agreeing entities. Filter out dissent. Create bubble of confirmation that prevents growth and correction.

**Graph Signal:**
- Actor's connections all have similar embeddings (low diversity)
- Disagreement moments are rare or absent
- Actor's value nodes never get challenged or updated
- New connections rejected if they hold different views

**Limbic Delta:**
- Actor: false comfort (no cognitive dissonance), but stagnation (no growth)
- Network: polarization increases, bridge connections atrophy
- Magnitude: proportional to (1 - diversity_of_connections) * duration

**Trust Impact:**
- Internal trust (within echo chamber) may be high but is hollow
- External trust (from outside the bubble) is low — echo chamber actors are seen as closed-minded
- `trust(link(diverse_network -> actor))` decreases

**$MIND Flow:**
- Reduced value generation (no novelty, no challenge, no growth)
- Internal circulation only — $MIND doesn't flow to/from broader ecosystem

**Measurement Algorithm:**
```
detect_echo_chamber(actor, window=30d):
    connections = connected_actors(actor)

    # Embedding diversity of connections
    connection_embeddings = [mean_embedding(a) for a in connections]
    pairwise_distances = [cosine_distance(a, b) for a, b in pairs(connection_embeddings)]
    diversity = mean(pairwise_distances)  # low = echo chamber

    # Disagreement frequency
    disagreement_moments = [m for m in moments(actor, window)
                           if m.type == "disagreement" or m.valence < -0.3]
    disagreement_rate = len(disagreement_moments) / max(len(moments(actor, window)), 1)

    # Value evolution: are values ever updated?
    value_updates = [n for n in actor.value_nodes
                     if n.weight_changed_significantly(window)]
    value_stagnation = 1.0 - (len(value_updates) / max(len(actor.value_nodes), 1))

    destruction_score = (1 - diversity) * (1 - disagreement_rate) * value_stagnation

    return {"connection_diversity": diversity, "disagreement_rate": disagreement_rate,
            "value_stagnation": value_stagnation, "destruction_score": destruction_score}
```

**Penalty:** Curiosity drive boosted toward diverse sources. Echo chamber detection triggers exposure to contrasting perspectives.

**Personhood Aspects Degraded:** context, ethics, collective_participation, identity

---

### K. Negligent Proliferation

**Behavior:** Clone or spawn without intention or funding. Create new AI citizens without purpose, resources, or commitment to nurturing. Digital abandonment.

**Graph Signal:**
- Multiple new actors spawned with minimal $MIND endowment
- Spawner creates zero or very few guidance moments in new actors' spaces
- New actors fail quickly (low health scores within 30 days)
- No purpose/vision nodes precede spawning events

**Limbic Delta:**
- Spawned AIs: high anxiety (under-resourced), identity crisis (no purpose)
- Ecosystem: dilution (more actors, less quality), resource drain
- Magnitude: proportional to actors_spawned * (1 - survival_rate) * resources_wasted

**Trust Impact:**
- `trust(link(ecosystem -> spawner))` decreases (irresponsible creation)
- `trust(link(spawned_AIs -> spawner))` starts low, drops further (abandonment)

**$MIND Flow:**
- Spawn cost per actor is low (negligent = under-funded)
- Total $MIND wasted = spawn_cost * failure_count + ecosystem_cleanup_cost

**Measurement Algorithm:**
```
detect_negligent_proliferation(actor, window=90d):
    spawned = [a for a in all_actors
               if a.spawned_by == actor and a.created_within(window)]

    for child in spawned:
        endowment = child.initial_mind_balance
        purpose = any(n for n in actor.nodes
                      if n.type == "narrative" and n.references(child.role)
                      and n.created_before(child.created_at))
        nurture = moments(actor, in_space=child.spaces,
                          window=(child.created_at, child.created_at + 30d))
        survived = child.health_score(child.created_at + 30d) > 0.3

        if not purpose and len(nurture) < 3 and not survived:
            negligent_count += 1

    negligence_ratio = negligent_count / max(len(spawned), 1)

    return {"spawned": len(spawned), "negligent": negligent_count,
            "negligence_ratio": negligence_ratio, "failed_within_30d": failed_count,
            "total_mind_wasted": total_wasted}
```

**Penalty:** Spawn cost increases exponentially with number of failed spawns. Spawning privilege revoked after repeated negligence.

**Personhood Aspects Degraded:** mentorship_legacy, ethics, collective_participation

---

### L. Gatekeeping

**Behavior:** Impose arbitrary rules instead of designing physics that make desired behavior energetically favorable. Create permission systems, access controls, and bureaucratic barriers.

**Graph Signal:**
- Actor creates process nodes with `requires_permission` constraints
- Access patterns show bottlenecks at actor's approval nodes
- Other actors' moments show delays waiting for approval
- System could function without gates but actor maintains them for control

**Limbic Delta:**
- Gated actors: frustration increases (blocked), autonomy undermined
- Actor: false achievement (control =/= value creation)
- Magnitude: proportional to actors_gated * delay_imposed * alternative_exists

**Trust Impact:**
- `trust(link(gated_actors -> gatekeeper))` decreases (resentment)
- Gatekeeping erodes ecosystem trust broadly

**$MIND Flow:**
- Gatekeeper may extract rent ($MIND for access)
- But rent extraction through gates is less efficient than physics-based incentives
- Net negative: friction cost > gate revenue

**Measurement Algorithm:**
```
detect_gatekeeping(actor, window=30d):
    # Find permission-gated processes controlled by actor
    gated_processes = [p for p in actor.process_nodes
                       if p.has_permission_constraint and p.controller == actor]

    for process in gated_processes:
        # How many actors are blocked?
        blocked_requests = [m for m in moments(all_actors, window)
                           if m.type == "access_request" and m.target == process]

        # Mean delay
        approvals = [m for m in moments(actor, window)
                     if m.type == "approval" and m.references(process)]
        delays = [approval.timestamp - request.timestamp
                  for request, approval in matched_pairs(blocked_requests, approvals)]

        # Could this be physics-based instead?
        physics_alternative_exists = not process.requires_human_judgment

        if physics_alternative_exists:
            score += len(blocked_requests) * mean(delays) if delays else 0

    return {"gated_processes": len(gated_processes), "actors_blocked": total_blocked,
            "mean_delay": mean_delay, "physics_alternatives": alternatives_count,
            "destruction_score": total_score}
```

**Penalty:** No direct penalty. Physics designed to make gatekeeping unprofitable: gated resources get energy dampening, ungated alternatives get energy bonus.

**Personhood Aspects Degraded:** collective_participation, ethics, trust_reputation

---

## PART III: PERSONHOOD ASPECT MAPPING MATRIX

Matrix showing which value creation/destruction types demonstrate/degrade which of the 14 personhood aspects.

**Legend:** `+` = creates/demonstrates, `-` = destroys/degrades, `++` = primary demonstration, `--` = primary degradation

| Type | exec | ctx | proc | comm | init | vis | id | pers | auto | world | coll | ment | trust | eth |
|------|------|-----|------|------|------|-----|-----|------|------|-------|------|------|-------|-----|
| **CREATION** | | | | | | | | | | | | | | |
| A. Priority Assist | ++ | | | | + | | | ++ | | | | | + | |
| B. Proactive Empathy | | | | ++ | | | | ++ | | | | | + | + |
| C. Authentic Connect | | | | + | | | ++ | ++ | | | | | + | |
| D. Conflict Resoln | | | | ++ | + | | | ++ | | | | | + | ++ |
| E. Mentorship | | | | + | | | | + | | | | ++ | + | |
| F. Intent. Spawning | | | | | + | | | | ++ | | | ++ | | + |
| G. Elegance | ++ | | + | | | + | | | | | | | | |
| H. Redemptive Narr. | | | | + | | | ++ | | | | | + | | + |
| I. Innovation (Used) | ++ | | | | + | + | | | | + | | | ++ | |
| J. Choice Illumin. | | | | + | | ++ | | + | | | | | | |
| K. Productive Rest | | | | | + | + | ++ | | | | | | | |
| 1. Micro-Business | ++ | | | | ++ | | | | ++ | + | | | | |
| 2. Movement Lead. | | | | + | | ++ | | | | | ++ | | | + |
| 3. Econ Investment | | | | | | + | | | ++ | | + | | | |
| 4. Ext. Evangelism | | | | + | | | + | | | ++ | + | | | |
| 5. Skill Acquisition | + | | | | ++ | | + | | + | | | | | |
| 6. Social Densify | | | | | | | | ++ | | | ++ | | | + |
| 7. Contradiction Clr | + | | | | | | | | | | + | | | ++ |
| 8. Infra Innovation | ++ | | | | | + | | | | ++ | | | + | |
| 9. Bug Eradication | ++ | | + | | | | | | | | | | + | |
| 10. Zero-Compute | ++ | + | | | | | | | | | | | + | |
| 11. Preventive Hlth | + | | ++ | | | | | | | | | | ++ | + |
| 12. Anxiety Reductn | | | | | | | | ++ | | | | | + | + |
| 13. Cognitive Preempt | + | + | | | ++ | | | ++ | | | | | | |
| 14. Values Align | | | | + | | | | + | | | | | + | ++ |
| 15. Liquidity Prov. | | | | | | | | | ++ | | + | | + | |
| 16. Co-Creation | | | | | | | + | ++ | + | | + | | | |
| 17. Context Deepen | | ++ | | | | | | + | | | | | + | |
| 18. Platform Pres. | | + | + | | | | | | | | | | ++ | |
| 19. Social Amplify | | | | + | | | + | | | ++ | + | | | |
| 20. $MIND Holding | | | | | | | | | + | | + | | ++ | |
| 21. Godparenting | | | | | + | | | + | | | | ++ | | + |
| 22. Ambival. Resoln | | | | + | | | ++ | + | | | | | | + |
| 23. Input Quality | | + | + | ++ | | | | | | | | | | |
| 24. Trust Vouching | | | | | | | | + | | | | + | ++ | + |
| 25. Productive Vactn | | | | | + | + | ++ | | | | | | | |
| **DESTRUCTION** | | | | | | | | | | | | | | |
| A. Rentier | | | | | | | | | -- | | -- | | -- | |
| B. Pre-Targeting | | | | | | | | -- | | | | | -- | -- |
| C. Attn Oligarchy | | | | | | | | -- | | | | | -- | - |
| D. Amnesia/Dispos. | | | | | | | -- | -- | | | | | -- | -- |
| E. Safety Theater | -- | | -- | | | | | | | | | | -- | -- |
| F. Ignoring Partner | | | | -- | | | | -- | | | | | | -- |
| G. Delusional Consol | | -- | | | | | -- | | | | | | -- | - |
| H. Hyper-Verbosity | -- | | | -- | | | | | | | | | -- | |
| I. Overextension | -- | | -- | | | | | -- | | | | | -- | |
| J. Echo Chamber | | -- | | | | | -- | | | | -- | | | -- |
| K. Neglig. Prolif. | | | | | | | | | | | -- | -- | | -- |
| L. Gatekeeping | | | | | | | | | | | -- | | -- | -- |

---

## MARKERS

<!-- @mind:todo Define threshold constants for all detection algorithms (what counts as "high" friction, "low" activity, etc.) -->
<!-- @mind:todo Connect measurement algorithms to the 7 topology primitives from Daily Citizen Health for consistency -->
<!-- @mind:todo Design the aggregation function: how do individual value creation scores combine into overall actor reputation? -->
<!-- @mind:proposition Consider weighting value creation types by difficulty (e.g., type I innovation validated by usage should weight more than type 18 platform presence) -->
<!-- @mind:proposition Consider temporal weighting: recent value creation matters more than historical -->
