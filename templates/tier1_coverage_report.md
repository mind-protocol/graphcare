# Test Coverage Report - {{client_name}}

**Generated:** {{generation_timestamp}}
**Coverage Tool:** {{coverage_tool}}
**Overall Coverage:** {{overall_coverage}}%

{{#if coverage_status}}
**Status:** {{coverage_status_emoji}} {{coverage_status}}
{{/if}}

---

## Executive Summary

**Coverage Breakdown:**
- **Line Coverage:** {{line_coverage}}%
- **Branch Coverage:** {{branch_coverage}}%
- **Function Coverage:** {{function_coverage}}%
- **Statement Coverage:** {{statement_coverage}}%

**Quality Gates:**
{{#each quality_gates}}
- {{gate_name}}: {{#if passed}}✅ PASS{{else}}❌ FAIL{{/if}} ({{current_value}} / {{threshold}} required)
{{/each}}

**Trend:** {{coverage_trend_emoji}} {{coverage_trend_description}}

---

## Coverage by Component

{{#each components}}
### {{component_name}}

**Overall:** {{overall_coverage}}% | **Line:** {{line_coverage}}% | **Branch:** {{branch_coverage}}%

{{#if critical_path}}
⚠️ **Critical Path Component** - Higher coverage standards apply (target: {{critical_path_target}}%)
{{/if}}

**Files:**
{{#each files}}
| File | Lines | Coverage | Status |
|------|-------|----------|--------|
| `{{file_path}}` | {{total_lines}} | {{coverage_percentage}}% | {{status_emoji}} |
{{/each}}

**Untested Functions:**
{{#if untested_functions}}
{{#each untested_functions}}
- `{{function_name}}` in `{{file_path}}:{{line_number}}`
  {{#if complexity}}- Complexity: {{complexity}}/10{{/if}}
  {{#if risk_level}}- Risk: {{risk_level}}{{/if}}
{{/each}}
{{else}}
_All functions have test coverage_ ✅
{{/if}}

**Coverage Gaps:**
{{#if gaps}}
{{#each gaps}}
- {{gap_description}}
  - Location: `{{file_path}}:{{start_line}}-{{end_line}}`
  - Priority: {{priority}}
  - Recommendation: {{recommendation}}
{{/each}}
{{else}}
_No significant coverage gaps detected_ ✅
{{/if}}

---

{{/each}}

## Critical Paths Analysis

{{#each critical_paths}}
### {{path_name}}

**Coverage:** {{coverage_percentage}}% {{status_emoji}}
**Risk Level:** {{risk_level}}
**Target Coverage:** {{target_coverage}}%

**Path Flow:**
{{#each steps}}
{{step_number}}. `{{function_name}}` ({{file_path}}) - {{coverage}}%
{{/each}}

{{#if gaps}}
**Gaps to Address:**
{{#each gaps}}
- {{gap_description}}
{{/each}}
{{/if}}

{{#if recommendations}}
**Recommendations:**
{{#each recommendations}}
- {{recommendation}}
{{/each}}
{{/if}}

---

{{/each}}

## Test Suite Health

**Total Tests:** {{total_tests}}
**Test Distribution:**
{{#each test_distribution}}
- {{test_type}}: {{count}} tests ({{percentage}}%)
{{/each}}

**Test Quality Indicators:**
- **Avg assertions per test:** {{avg_assertions}}
- **Avg test runtime:** {{avg_runtime}}ms
- **Flaky tests:** {{flaky_test_count}}
- **Skipped tests:** {{skipped_test_count}}

**Test Files:**
{{#each test_files}}
| File | Tests | Coverage Contributed | Status |
|------|-------|---------------------|--------|
| `{{file_path}}` | {{test_count}} | {{coverage_contributed}}% | {{status_emoji}} |
{{/each}}

---

## Coverage Trends

{{#if historical_data}}
**Last 30 Days:**

```
{{coverage_trend_chart}}
```

**Changes:**
- **Week over week:** {{wow_change}}% {{wow_emoji}}
- **Month over month:** {{mom_change}}% {{mom_emoji}}

**Recent Commits Impact:**
{{#each recent_commits}}
- `{{commit_hash}}` - {{coverage_change}}% ({{coverage_before}}% → {{coverage_after}}%)
{{/each}}

{{else}}
_No historical data available (first extraction)_
{{/if}}

---

## Recommendations

### High Priority

{{#each high_priority_recommendations}}
{{priority_number}}. **{{title}}**
   - **Impact:** {{impact_description}}
   - **Effort:** {{effort_estimate}}
   - **Action:** {{action_description}}
   - **Files:** {{#each affected_files}}`{{this}}`{{#unless @last}}, {{/unless}}{{/each}}

{{/each}}

### Medium Priority

{{#each medium_priority_recommendations}}
- **{{title}}** - {{description}}
{{/each}}

### Low Priority (Tech Debt)

{{#each low_priority_recommendations}}
- {{description}}
{{/each}}

---

## Validation Gap Analysis

**Behaviors Without Tests:**
{{#if behaviors_without_tests}}
{{#each behaviors_without_tests}}
### {{behavior_name}}

**Spec:** {{spec_description}}
**Implementation:** `{{implementation_file}}:{{line_number}}`
**Risk:** {{risk_level}}

**Recommended Tests:**
{{#each recommended_tests}}
- {{test_description}}
{{/each}}

---

{{/each}}
{{else}}
_All documented behaviors have test coverage_ ✅
{{/if}}

**Tests Without Behavior Specs:**
{{#if orphan_tests}}
{{#each orphan_tests}}
- `{{test_name}}` in `{{test_file}}`
  - Recommendation: {{recommendation}}
{{/each}}
{{else}}
_All tests map to documented behaviors_ ✅
{{/if}}

---

## Coverage Heatmap

**By Directory:**

{{#each directory_coverage}}
| Directory | Files | Coverage | Status |
|-----------|-------|----------|--------|
| `{{directory_path}}` | {{file_count}} | {{coverage_percentage}}% | {{status_emoji}} |
{{/each}}

**Hotspots (Low Coverage + High Complexity):**
{{#if hotspots}}
{{#each hotspots}}
- `{{file_path}}` - {{coverage}}% coverage, {{complexity}}/10 complexity
  - **Risk:** {{risk_description}}
  - **Action:** {{recommended_action}}
{{/each}}
{{else}}
_No hotspots detected_ ✅
{{/if}}

---

## Query to Regenerate This Report

```cypher
MATCH (artifact:U4_Code_Artifact)
WHERE artifact.artifact_type = 'source'
OPTIONAL MATCH (artifact)-[:U4_TESTED_BY]->(test:U4_Code_Artifact)
OPTIONAL MATCH (artifact)-[:U4_HAS_METRIC]->(metric:U4_Metric)
OPTIONAL MATCH (metric)-[:U4_MEASURED_BY]->(measurement:U4_Measurement)
WHERE metric.metric_type = 'coverage'
RETURN artifact, collect(test), collect(measurement)
ORDER BY artifact.path
```

---

**Report Generated By:** Vera "Truth-Teller" (Chief Validator, GraphCare)

**Last Updated:** {{last_updated}}

**Legend:**
- ✅ Excellent (≥90%)
- 🟢 Good (80-89%)
- 🟡 Acceptable (70-79%)
- 🟠 Needs Attention (60-69%)
- 🔴 Critical (<60%)
