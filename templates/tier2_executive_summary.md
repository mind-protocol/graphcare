# Executive Summary - {{client_name}}

**Prepared For:** {{executive_audience}}
**Prepared By:** Sage (Chief Documenter, GraphCare) + Mel (Chief Care Coordinator)
**Date:** {{preparation_date}}
**Graph Extraction Date:** {{extraction_date}}

---

## What This System Does

[**SAGE WRITES:** 2-3 paragraph summary for non-technical executives]

[Template guidance:
- What problem does this system solve?
- Who are the users?
- What is the business value?
- What are the key capabilities?
- Avoid technical jargon - use business language]

**Example:**
> This system manages [BUSINESS_FUNCTION]. It serves [USER_TYPES] by enabling them to [KEY_CAPABILITIES]. The system processes [SCALE_METRICS] and integrates with [EXTERNAL_SYSTEMS]. It is critical to [BUSINESS_OUTCOMES].

---

## System Health Overview

**Overall Assessment:** {{health_status_emoji}} {{health_status_text}}

**Key Metrics:**
- **Code Coverage:** {{overall_coverage}}% {{coverage_emoji}}
- **Security Status:** {{security_status}}
- **Technical Debt:** {{tech_debt_level}}
- **Documentation Quality:** {{documentation_quality_score}}/10

{{#if critical_issues}}
**Critical Issues Requiring Attention:**
{{#each critical_issues}}
- {{issue_description}} (Impact: {{business_impact}})
{{/each}}
{{/if}}

---

## Architecture at a Glance

[**SAGE WRITES:** Non-technical architecture explanation]

[Template guidance:
- Describe architecture in business terms, not technical terms
- Use analogies if helpful
- Focus on WHY this architecture was chosen
- Highlight any architectural risks or strengths]

**Example:**
> The system is built as [ARCHITECTURE_TYPE_IN_PLAIN_ENGLISH]. Think of it as [ANALOGY]. This design provides [BUSINESS_BENEFITS] but requires [TRADEOFFS].

**Major Components:**
{{#each major_components}}
- **{{component_name}}:** {{business_description}}
{{/each}}

---

## What's Working Well

[**SAGE WRITES:** Highlight strengths]

[Template guidance:
- What are the system's strengths?
- What's well-documented?
- What has good test coverage?
- What shows good architectural decisions?
- Frame positively but truthfully]

**Example strengths:**
- ✅ Strong test coverage in critical payment workflows (92%)
- ✅ Clear architectural separation between business logic and data access
- ✅ Comprehensive API documentation for all public endpoints
- ✅ Security best practices followed for authentication

---

## What Needs Attention

[**SAGE WRITES:** Prioritized list of concerns]

[Template guidance:
- Prioritize by business impact, not technical severity
- High priority = affects customers/revenue/compliance
- Medium priority = technical debt, maintainability
- Low priority = nice-to-haves
- For each item: What's the risk? What's the fix? What's the cost?]

### High Priority

{{#each high_priority_concerns}}
#### {{concern_number}}. {{concern_title}}

**What's the issue?** {{issue_description_plain_english}}

**Why does it matter?** {{business_impact}}

**What should we do?** {{recommendation}}

**Estimated effort:** {{effort_estimate}}

{{/each}}

### Medium Priority

{{#each medium_priority_concerns}}
- **{{concern_title}}** - {{brief_description}}
{{/each}}

### Low Priority (Tech Debt)

{{#each low_priority_concerns}}
- {{brief_description}}
{{/each}}

---

## Strategic Recommendations

[**MEL WRITES:** Strategic perspective from care coordinator]

[Template guidance:
- What investments would yield highest ROI?
- What are the biggest risks?
- What should be prioritized for next quarter?
- How does this compare to similar systems?
- What opportunities exist?]

### Near-Term (Next Quarter)

{{#each near_term_recommendations}}
{{rank}}. **{{recommendation_title}}**
   - **Why:** {{strategic_rationale}}
   - **Impact:** {{expected_outcome}}
   - **Investment:** {{time_and_resource_estimate}}

{{/each}}

### Long-Term (6-12 Months)

{{#each long_term_recommendations}}
- **{{recommendation_title}}** - {{brief_description}}
{{/each}}

---

## Comparison to Industry Standards

[**SAGE WRITES:** Benchmark against typical systems]

[Template guidance:
- How does coverage compare to industry standards?
- How does architecture compare to modern best practices?
- How does security posture compare?
- Frame objectively, not judgmentally]

| Metric | {{client_name}} | Industry Average | Assessment |
|--------|-----------------|------------------|------------|
| Test Coverage | {{coverage}}% | 70-80% | {{coverage_assessment}} |
| Code Documentation | {{docs_score}}/10 | 7/10 | {{docs_assessment}} |
| Security Posture | {{security_score}}/10 | 8/10 | {{security_assessment}} |
| Tech Debt Level | {{debt_score}}/10 | 6/10 | {{debt_assessment}} |

---

## Investment Priorities

[**MEL WRITES:** Resource allocation guidance]

[Template guidance:
- Where should they invest development time?
- Where should they invest in training?
- Where should they invest in tooling?
- What are the opportunity costs of NOT investing?]

**Recommended Budget Allocation:**

{{#each budget_recommendations}}
- **{{category}}:** {{recommended_percentage}}% of engineering capacity
  - {{justification}}
{{/each}}

---

## Next Steps

[**SAGE + MEL WRITE:** Actionable next steps]

### Immediate (This Week)

{{#each immediate_actions}}
- [ ] {{action_description}}
  - Owner: {{recommended_owner}}
  - Duration: {{estimated_duration}}
{{/each}}

### Short-Term (This Month)

{{#each short_term_actions}}
- [ ] {{action_description}}
{{/each}}

### Long-Term (This Quarter)

{{#each long_term_actions}}
- [ ] {{action_description}}
{{/each}}

---

## Questions This Report Answers

[**SAGE WRITES:** Executive FAQ]

**Q: Is this system secure?**
A: {{security_answer}}

**Q: Can we scale if we grow 10x?**
A: {{scalability_answer}}

**Q: What are the biggest risks?**
A: {{risk_answer}}

**Q: How does our system compare to competitors?**
A: {{competitive_answer}}

**Q: What would it take to modernize this system?**
A: {{modernization_answer}}

---

## About This Report

This executive summary was generated from a comprehensive knowledge graph extraction of {{client_name}}'s codebase and documentation. The graph contains {{node_count}} nodes and {{link_count}} relationships, representing the complete structure of the system.

**For more detail, see:**
- [Technical Architecture Overview](./architecture_overview.md) - For technical leads
- [Developer Onboarding Guide](./onboarding_guide.md) - For new team members
- [API Reference](./api_reference.md) - For integration partners
- [Coverage Report](./coverage_report.md) - For QA and testing teams

**Interactive Exploration:**
Visit [docs.{{client_domain}}.mindprotocol.ai](https://docs.{{client_domain}}.mindprotocol.ai) to explore the knowledge graph interactively.

---

**Report Authors:**
- **Sage** (Chief Documenter, GraphCare) - Documentation synthesis
- **Mel** (Chief Care Coordinator, GraphCare) - Strategic recommendations

**Reviewed By:**
- {{#each reviewers}}{{name}} ({{role}}){{/each}}

**Confidentiality:** {{confidentiality_level}}

**Last Updated:** {{last_updated}}
