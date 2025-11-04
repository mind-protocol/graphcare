# Developer Onboarding Guide - {{client_name}}

**Welcome!** This guide will get you from zero to productive in {{estimated_onboarding_time}}.

**Prepared By:** Sage (Chief Documenter, GraphCare)
**Last Updated:** {{last_updated}}

---

## Your First Week

### Day 1: Get Running

#### Set Up Your Development Environment

**Prerequisites:**
{{#each prerequisites}}
- {{tool_name}} ({{version}}) - {{why_needed}}
{{/each}}

**Installation Steps:**

```bash
# 1. Clone the repository
{{clone_command}}

# 2. Install dependencies
{{install_dependencies_command}}

# 3. Set up environment variables
{{env_setup_command}}

# 4. Run database migrations (if applicable)
{{migration_command}}

# 5. Start the development server
{{start_dev_server_command}}
```

**Expected Output:**
```
{{expected_output_example}}
```

**If you see errors:**
{{#each common_setup_errors}}
- **Error:** `{{error_message}}`
  - **Fix:** {{fix_description}}
{{/each}}

**Verify it works:**
{{#each verification_steps}}
{{step_number}}. {{step_description}}
   - Expected result: {{expected_result}}
{{/each}}

✅ **Success:** When you see {{success_indicator}}, you're ready to code!

---

#### Understand the Big Picture

**What does this system do?**

{{system_purpose_plain_english}}

**Who are the users?**

{{#each user_types}}
- **{{user_type}}:** {{user_description}}
{{/each}}

**What are the core use cases?**

{{#each core_use_cases}}
{{use_case_number}}. {{use_case_title}}
   - User action: {{user_action}}
   - System response: {{system_response}}
   - See code in: `{{primary_file}}`
{{/each}}

**Architecture in 60 seconds:**

{{architecture_elevator_pitch}}

[Read more: [Architecture Narrative](./tier2_architecture_narrative.md)]

---

### Day 2-3: Make Your First Change

#### Your First Task: {{first_task_suggestion}}

**Why this task?** {{task_rationale}}

**What you'll learn:**
{{#each learning_objectives}}
- {{objective}}
{{/each}}

**Step-by-step guide:**

**1. Find the code**

The {{feature_name}} feature lives in:
{{#each relevant_files}}
- `{{file_path}}` - {{file_purpose}}
{{/each}}

**Pro tip:** Use the interactive graph explorer to find related code:
[Search: "{{search_query}}"](https://docs.{{client_domain}}.mindprotocol.ai/search?q={{encoded_search_query}})

**2. Understand the current behavior**

{{current_behavior_description}}

**Code walkthrough:**

```{{language}}
{{code_walkthrough}}
```

**3. Make the change**

{{change_description}}

**Code to modify:**

```{{language}}
// File: {{file_to_modify}}:{{line_number}}

// OLD CODE:
{{old_code}}

// NEW CODE:
{{new_code}}

// WHY: {{change_rationale}}
```

**4. Write tests**

{{testing_guidance}}

**Test to add:**

```{{language}}
// File: {{test_file}}

{{test_code}}
```

**5. Run tests and verify**

```bash
{{test_command}}
```

**Expected:** All tests pass ✅

**6. Submit for review**

```bash
{{pr_submission_commands}}
```

**Code review expectations:**
{{#each code_review_expectations}}
- {{expectation}}
{{/each}}

---

### Day 4-5: Explore the System

#### Key Areas to Understand

{{#each key_areas}}
##### {{area_number}}. {{area_name}}

**What it does:** {{area_description}}

**Key files:**
{{#each files}}
- `{{file_path}}`
{{/each}}

**How to explore:**
{{#each exploration_tips}}
- {{tip}}
{{/each}}

**Try this query:**
[{{query_description}}](https://docs.{{client_domain}}.mindprotocol.ai/query?q={{encoded_query}})

---

{{/each}}

---

## Week 2: Mastering Common Tasks

### How to Add a New Feature

[**SAGE PROVIDES:** Step-by-step workflow for feature development]

**1. Understand the requirement**
- [ ] Read spec/ADR (if exists): {{typical_spec_location}}
- [ ] Clarify with {{stakeholder_role}}
- [ ] Identify affected components

**2. Design the change**
- [ ] Which layers are affected? {{layer_guidance}}
- [ ] What data changes? {{data_guidance}}
- [ ] What tests are needed? {{test_guidance}}

**3. Implement**
- [ ] Follow {{coding_standard_link}}
- [ ] Add inline comments for non-obvious logic
- [ ] Update API docs if adding endpoints

**4. Test**
- [ ] Unit tests for new functions
- [ ] Integration tests for new workflows
- [ ] Manual testing checklist: {{manual_test_checklist_link}}

**5. Document**
- [ ] Update README if user-facing
- [ ] Add/update ADR if architectural change
- [ ] Update API reference if endpoint added

**6. Submit**
- [ ] Create PR with template: {{pr_template_link}}
- [ ] Request review from {{typical_reviewers}}
- [ ] Address feedback
- [ ] Merge when approved

---

### How to Fix a Bug

**1. Reproduce**
```bash
{{bug_reproduction_guidance}}
```

**2. Find the code**

**Strategy 1: Follow the stack trace**
{{#if typical_stack_trace}}
```
{{typical_stack_trace}}
```
{{/if}}

**Strategy 2: Search the graph**
- Go to [Graph Explorer](https://docs.{{client_domain}}.mindprotocol.ai/graph)
- Search for: {{search_strategy}}
- Look for: {{what_to_look_for}}

**Strategy 3: Ask experienced developers**
{{#each experienced_developers}}
- {{name}} - Expert in {{expertise_area}}
{{/each}}

**3. Write a failing test**

```{{language}}
{{failing_test_example}}
```

**4. Fix the bug**

Common bug patterns in this codebase:
{{#each common_bug_patterns}}
- **{{pattern_name}}:** {{pattern_description}}
  - How to fix: {{fix_strategy}}
{{/each}}

**5. Verify the fix**
- [ ] Failing test now passes
- [ ] No regressions (full test suite passes)
- [ ] Manual verification

**6. Submit with clear description**

PR title format: `fix: {{bug_description}}`

PR body should include:
- Bug description
- Root cause analysis
- Fix explanation
- Test added

---

### How to Add Tests

**Testing philosophy:** {{testing_philosophy}}

**Test types in this codebase:**
{{#each test_types}}
- **{{test_type}}:** {{test_type_description}}
  - Location: `{{test_location}}`
  - Run with: `{{test_command}}`
{{/each}}

**Example test patterns:**

```{{language}}
{{test_pattern_examples}}
```

**Coverage expectations:**
- New code: {{new_code_coverage_target}}%
- Critical paths: {{critical_path_coverage_target}}%
- Overall target: {{overall_coverage_target}}%

---

## Common Workflows

### Workflow 1: Adding a New API Endpoint

{{#each api_workflow_steps}}
{{step_number}}. {{step_title}}
   ```{{language}}
   {{code_example}}
   ```
   {{explanation}}

{{/each}}

---

### Workflow 2: Modifying Database Schema

{{#each db_schema_workflow_steps}}
{{step_number}}. {{step_title}}
   {{explanation}}
   {{#if command}}
   ```bash
   {{command}}
   ```
   {{/if}}

{{/each}}

---

### Workflow 3: Integrating External Service

{{#each external_service_workflow_steps}}
{{step_number}}. {{step_title}}
   {{explanation}}

{{/each}}

---

## The Codebase Map

### Where to Find Things

{{#each codebase_sections}}
#### {{section_name}}

**Purpose:** {{section_purpose}}

**Key directories:**
{{#each directories}}
- `{{directory_path}}` - {{directory_description}}
{{/each}}

**Key files:**
{{#each key_files}}
- `{{file_path}}` - {{file_description}}
{{/each}}

**When to work here:**
{{#each when_to_work_here}}
- {{scenario}}
{{/each}}

---

{{/each}}

### Navigation Tips

**Find by feature:**
{{#each features_to_files}}
- {{feature_name}} → `{{file_path}}`
{{/each}}

**Find by domain:**
{{#each domains_to_modules}}
- {{domain_name}} → {{module_names}}
{{/each}}

**Find related code:**
Use the [Dependency Graph](https://docs.{{client_domain}}.mindprotocol.ai/dependencies) to see what depends on what.

---

## Team Conventions

### Code Style

**Language:** {{primary_language}}
**Style guide:** {{style_guide_link}}

**Key conventions:**
{{#each code_conventions}}
- **{{convention_name}}:** {{convention_description}}
  {{#if example}}
  ```{{language}}
  {{example}}
  ```
  {{/if}}
{{/each}}

**Linting:**
```bash
{{lint_command}}
```

**Formatting:**
```bash
{{format_command}}
```

---

### Git Workflow

**Branch naming:**
- `feature/{{feature-name}}` - New features
- `fix/{{bug-name}}` - Bug fixes
- `refactor/{{what-refactored}}` - Refactoring
- `docs/{{what-documented}}` - Documentation

**Commit messages:**
{{commit_message_format}}

**PR process:**
{{#each pr_process_steps}}
{{step_number}}. {{step_description}}
{{/each}}

---

### Communication

**Where to ask questions:**
{{#each communication_channels}}
- **{{channel_name}}:** {{channel_purpose}}
{{/each}}

**Who to ask:**
{{#each team_members}}
- **{{name}}** ({{role}}) - Expert in: {{expertise}}
{{/each}}

**When to ask:**
{{when_to_ask_guidance}}

---

## Troubleshooting

### Common Issues

{{#each common_issues}}
#### {{issue_title}}

**Symptoms:** {{symptoms}}

**Cause:** {{cause}}

**Fix:**
{{#each fix_steps}}
{{step_number}}. {{step_description}}
{{/each}}

---

{{/each}}

### Debugging Tips

**Logging:**
{{logging_guidance}}

**Breakpoints:**
{{breakpoint_guidance}}

**Performance profiling:**
{{profiling_guidance}}

---

## Resources

### Essential Reading

{{#each essential_reading}}
- [{{title}}]({{link}}) - {{description}}
{{/each}}

### External Documentation

{{#each external_docs}}
- [{{tool_name}} Docs]({{link}})
{{/each}}

### Internal Links

- [Architecture Narrative](./tier2_architecture_narrative.md) - Deep-dive into system design
- [API Reference](./tier1_api_reference.md) - All endpoints documented
- [Code Reference](./tier1_code_reference.md) - All functions and classes
- [Interactive Graph](https://docs.{{client_domain}}.mindprotocol.ai) - Explore visually

---

## Feedback

**This guide is a living document.** If you found something unclear, confusing, or missing:

- Open an issue: {{issue_tracking_link}}
- Propose an edit: {{edit_link}}
- Ask in: {{feedback_channel}}

**Welcome to the team! You've got this.** 🚀

---

**Guide Author:** Sage (Chief Documenter, GraphCare)

**Contributors:**
{{#each contributors}}
- {{name}} ({{contribution}})
{{/each}}

**Last Updated:** {{last_updated}}
