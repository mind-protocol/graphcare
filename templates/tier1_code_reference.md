# Code Reference - {{client_name}}

**Generated:** {{generation_timestamp}}
**Total Files:** {{total_files}}
**Total Functions:** {{total_functions}}
**Total Classes:** {{total_classes}}

---

{{#each modules}}
## Module: {{module_path}}

**Description:** {{description}}
**Language:** {{language}}
**Lines of Code:** {{total_lines}}
**Complexity:** {{complexity_score}}/10

{{#if classes}}
### Classes

{{#each classes}}
#### `{{class_name}}`

**Location:** `{{file_path}}:{{line_number}}`
**Description:** {{description}}

{{#if inheritance}}
**Inherits From:**
{{#each inheritance}}
- `{{parent_class}}` {{#if file_path}}(from `{{file_path}}`){{/if}}
{{/each}}
{{/if}}

{{#if implemented_interfaces}}
**Implements:**
{{#each implemented_interfaces}}
- `{{interface_name}}`
{{/each}}
{{/if}}

**Properties:**
{{#if properties}}
{{#each properties}}
- `{{property_name}}`: {{property_type}} {{#if access_modifier}}({{access_modifier}}){{/if}}
  {{#if description}}_{{description}}_{{/if}}
{{/each}}
{{else}}
_No properties defined_
{{/if}}

**Methods:**
{{#if methods}}
{{#each methods}}
##### `{{method_name}}({{#each parameters}}{{name}}: {{type}}{{#unless @last}}, {{/unless}}{{/each}})` → `{{return_type}}`

**Location:** Line {{line_number}}
{{#if description}}**Description:** {{description}}{{/if}}
{{#if access_modifier}}**Access:** {{access_modifier}}{{/if}}

{{#if parameters}}
**Parameters:**
{{#each parameters}}
- `{{name}}` ({{type}}) - {{description}}
{{/each}}
{{/if}}

{{#if returns}}
**Returns:** {{returns.type}} - {{returns.description}}
{{/if}}

{{#if complexity}}**Complexity:** {{complexity}}/10{{/if}}
{{#if coverage}}**Coverage:** {{coverage}}%{{/if}}

{{#if calls}}
**Calls:**
{{#each calls}}
- `{{function_name}}` {{#if external}}(external: {{external_package}}){{/if}}
{{/each}}
{{/if}}

{{#if called_by}}
**Called By:**
{{#each called_by}}
- `{{function_name}}` in `{{file_path}}`
{{/each}}
{{/if}}

{{#if tests}}
**Tests:**
{{#each tests}}
- `{{test_name}}` in `{{test_file}}`
{{/each}}
{{/if}}

---

{{/each}}
{{else}}
_No methods defined_
{{/if}}

**Usage Example:**
```{{language}}
{{usage_example}}
```

---

{{/each}}
{{/if}}

{{#if functions}}
### Functions

{{#each functions}}
#### `{{function_name}}({{#each parameters}}{{name}}: {{type}}{{#unless @last}}, {{/unless}}{{/each}})` → `{{return_type}}`

**Location:** `{{file_path}}:{{line_number}}`
{{#if description}}**Description:** {{description}}{{/if}}

{{#if parameters}}
**Parameters:**
{{#each parameters}}
- `{{name}}` ({{type}}) - {{description}}
{{/each}}
{{/if}}

{{#if returns}}
**Returns:** {{returns.type}} - {{returns.description}}
{{/if}}

{{#if complexity}}**Complexity:** {{complexity}}/10{{/if}}
{{#if coverage}}**Coverage:** {{coverage}}%{{/if}}
{{#if risk_level}}**Risk Level:** {{risk_level}}{{/if}}

{{#if calls}}
**Calls:**
{{#each calls}}
- `{{function_name}}` {{#if external}}(external: {{external_package}}){{/if}}
{{/each}}
{{/if}}

{{#if called_by}}
**Called By:**
{{#each called_by}}
- `{{function_name}}` in `{{file_path}}`
{{/each}}
{{/if}}

{{#if tests}}
**Tests:**
{{#each tests}}
- `{{test_name}}` in `{{test_file}}`
{{/each}}
{{else}}
⚠️ **No tests found for this function**
{{/if}}

**Usage Example:**
```{{language}}
{{usage_example}}
```

---

{{/each}}
{{/if}}

{{#if constants}}
### Constants / Globals

{{#each constants}}
- `{{name}}` ({{type}}) = `{{value}}`
  {{#if description}}_{{description}}_{{/if}}
{{/each}}
{{/if}}

{{#if imports}}
### Dependencies

**Internal:**
{{#each internal_imports}}
- `{{import_path}}`
{{/each}}

**External:**
{{#each external_imports}}
- `{{package_name}}` ({{version}})
{{/each}}
{{/if}}

---

{{/each}}

## Index

### By File

{{#each files_index}}
- [`{{file_path}}`](#{{file_anchor}}) ({{function_count}} functions, {{class_count}} classes)
{{/each}}

### By Complexity

**High Complexity (≥7):**
{{#each high_complexity_functions}}
- `{{function_name}}` in `{{file_path}}` - Complexity: {{complexity}}/10
{{/each}}

**Medium Complexity (4-6):**
{{#each medium_complexity_functions}}
- `{{function_name}}` in `{{file_path}}` - Complexity: {{complexity}}/10
{{/each}}

### Untested Code

{{#each untested_functions}}
- `{{function_name}}` in `{{file_path}}` (Complexity: {{complexity}}, Risk: {{risk_level}})
{{/each}}

### API Endpoints

{{#each api_functions}}
- `{{http_method}} {{route}}` → `{{function_name}}` in `{{file_path}}`
{{/each}}

### Call Graph

**Most Called Functions:**
{{#each most_called}}
{{rank}}. `{{function_name}}` - Called {{call_count}} times
{{/each}}

**Leaf Functions (Call Nothing):**
{{#each leaf_functions}}
- `{{function_name}}` in `{{file_path}}`
{{/each}}

**Circular Dependencies:**
{{#if circular_dependencies}}
{{#each circular_dependencies}}
⚠️ Circular dependency detected:
{{#each cycle_path}}
- `{{function_name}}`
{{/each}}
{{/each}}
{{else}}
✅ No circular dependencies detected
{{/if}}

---

## Statistics

**Code Metrics:**
- Total Lines of Code: {{total_lines}}
- Average Function Length: {{avg_function_length}} lines
- Average Function Complexity: {{avg_complexity}}/10
- Average Functions per File: {{avg_functions_per_file}}

**Test Coverage:**
- Functions Tested: {{tested_functions}}/{{total_functions}} ({{tested_percentage}}%)
- Classes Tested: {{tested_classes}}/{{total_classes}} ({{tested_classes_percentage}}%)

**Complexity Distribution:**
- Low (1-3): {{low_complexity_count}} ({{low_complexity_percentage}}%)
- Medium (4-6): {{medium_complexity_count}} ({{medium_complexity_percentage}}%)
- High (7-10): {{high_complexity_count}} ({{high_complexity_percentage}}%)

**External Dependencies:**
- Total Packages: {{external_package_count}}
- With Known Vulnerabilities: {{vulnerable_package_count}}

---

## Query to Regenerate This Reference

```cypher
MATCH (artifact:U4_Code_Artifact)
WHERE artifact.artifact_type = 'source'
OPTIONAL MATCH (artifact)-[:GC_CONTAINS]->(func:GC_Function)
OPTIONAL MATCH (artifact)-[:GC_CONTAINS]->(class:GC_Class)
OPTIONAL MATCH (func)-[:GC_CALLS]->(called:GC_Function)
OPTIONAL MATCH (func)-[:U4_TESTED_BY]->(test:U4_Code_Artifact)
RETURN artifact, collect(func), collect(class), collect(called), collect(test)
ORDER BY artifact.path
```

---

**Reference Generated By:** Kai "The Surgeon" (Chief Engineer, GraphCare)

**Last Updated:** {{last_updated}}
