# API Reference - {{client_name}}

**Generated:** {{generation_timestamp}}
**Total Endpoints:** {{total_endpoints}}
**API Version:** {{api_version}}

---

{{#each api_categories}}
## {{category_name}}

{{#each endpoints}}
### {{method}} {{path}}

**Description:** {{description}}

**Implemented In:** `{{implementation_file}}:{{line_number}}`

{{#if deprecated}}
⚠️ **DEPRECATED** - {{deprecation_reason}}
**Use Instead:** {{replacement_endpoint}}
{{/if}}

#### Parameters

{{#if path_parameters}}
**Path Parameters:**
{{#each path_parameters}}
- `{{name}}` ({{type}}, required) - {{description}}
{{/each}}
{{/if}}

{{#if query_parameters}}
**Query Parameters:**
{{#each query_parameters}}
- `{{name}}` ({{type}}, {{#if required}}required{{else}}optional{{/if}}) - {{description}}
  {{#if default_value}}- Default: `{{default_value}}`{{/if}}
{{/each}}
{{/if}}

{{#if request_body}}
**Request Body:**
```json
{{request_body_schema}}
```
{{/if}}

#### Responses

{{#each responses}}
**{{status_code}} {{status_description}}**
```json
{{response_schema}}
```
{{#if example}}
**Example:**
```json
{{example}}
```
{{/if}}

{{/each}}

#### Error Codes

{{#each error_codes}}
- `{{code}}` - {{description}}
{{/each}}

#### Authentication

{{#if requires_auth}}
**Required:** Yes
**Method:** {{auth_method}}
**Scopes:** {{#each auth_scopes}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}
{{else}}
**Required:** No (public endpoint)
{{/if}}

#### Rate Limiting

{{#if rate_limit}}
**Limit:** {{rate_limit.requests}} requests per {{rate_limit.window}}
{{else}}
_No rate limiting configured_
{{/if}}

#### Usage Example

```bash
# cURL example
curl -X {{method}} \
  '{{base_url}}{{path}}{{#if example_query_params}}?{{example_query_params}}{{/if}}' \
  {{#if requires_auth}}-H 'Authorization: Bearer YOUR_TOKEN' \{{/if}}
  {{#if request_body}}-H 'Content-Type: application/json' \
  -d '{{example_request_body}}'{{/if}}
```

```python
# Python example
import requests

response = requests.{{method_lowercase}}(
    '{{base_url}}{{path}}'{{#if example_path_params_dict}}.format(**{{example_path_params_dict}}){{/if}},
    {{#if example_query_params_dict}}params={{example_query_params_dict}},{{/if}}
    {{#if request_body}}json={{example_request_body_dict}},{{/if}}
    {{#if requires_auth}}headers={'Authorization': 'Bearer YOUR_TOKEN'}{{/if}}
)
print(response.json())
```

#### Coverage

- **Line Coverage:** {{coverage.line_coverage}}%
- **Branch Coverage:** {{coverage.branch_coverage}}%
- **Tests:** {{test_count}} test(s)
{{#if test_files}}
  {{#each test_files}}- `{{this}}`
  {{/each}}
{{/if}}

#### Dependencies

**Calls:**
{{#if calls_functions}}
{{#each calls_functions}}
- `{{function_name}}` in `{{file_path}}`
{{/each}}
{{else}}
_No internal function calls detected_
{{/if}}

**External Services:**
{{#if external_services}}
{{#each external_services}}
- {{service_name}} ({{service_type}})
{{/each}}
{{else}}
_No external service calls_
{{/if}}

---

{{/each}}
{{/each}}

## API Health Metrics

**Total Endpoints:** {{total_endpoints}}
**Documented:** {{documented_count}} ({{documented_percentage}}%)
**Tested:** {{tested_count}} ({{tested_percentage}}%)
**Deprecated:** {{deprecated_count}}

**Coverage by Category:**
{{#each coverage_by_category}}
- **{{category_name}}:** {{coverage_percentage}}% ({{tested_endpoints}}/{{total_endpoints}} endpoints)
{{/each}}

**Authentication Distribution:**
{{#each auth_distribution}}
- {{auth_method}}: {{count}} endpoints
{{/each}}

---

**Query to regenerate this document:**
```cypher
MATCH (endpoint:GC_API_Endpoint)
OPTIONAL MATCH (endpoint)-[:GC_IMPLEMENTED_BY]->(func:GC_Function)
OPTIONAL MATCH (func)-[:GC_CALLS]->(dep:GC_Function)
OPTIONAL MATCH (endpoint)-[:U4_TESTED_BY]->(test:U4_Code_Artifact)
RETURN endpoint, func, collect(dep), collect(test)
ORDER BY endpoint.path
```

**Last Updated:** {{last_updated}}
