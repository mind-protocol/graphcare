# GraphCare Schema Specification

**Version:** 1.0.0
**Status:** Draft
**Created:** 2025-11-04
**Author:** Nora (Chief Architect)

---

## Overview

GraphCare extracts client knowledge graphs (codebases, documentation, decisions) into FalkorDB. This document defines:
- Node types (reused from Mind Protocol + GraphCare-specific)
- Link types (reused + custom)
- Citizen handoff contracts (what each citizen creates)
- Schema migration strategy

---

## Design Principles

### 1. Reuse Mind Protocol Types Where Possible

Mind Protocol has 33 node types and 34 link types designed for consciousness substrate. Many fit GraphCare's needs:
- `U4_Code_Artifact` - Source files (proven at scale)
- `U4_Knowledge_Object` - ADRs, specs, runbooks, guides
- `U4_Decision` - Decision records with rationale
- `U4_Metric` / `U4_Measurement` - Quality metrics
- `U4_Agent` - Developers, teams, orgs

**Rationale:** Proven types, standard attributes, interoperability with Mind Protocol tools.

### 2. GraphCare-Specific Types for Code Granularity

Mind Protocol doesn't need function-level or class-level nodes. GraphCare does:
- `GC_Function` - Individual functions/methods
- `GC_Class` - Classes/interfaces/types
- `GC_Module` - Modules/packages
- `GC_API_Endpoint` - REST/GraphQL endpoints

**Rationale:** Clients need function-level traceability, dependency graphs, call graphs.

### 3. All GraphCare Nodes are L2 (Organizational)

- `level` = "L2" for all GraphCare-created nodes
- `scope_ref` = client organization ID (e.g., "client_acme_corp")
- Aligns with Mind Protocol's L1 (personal), L2 (org), L3 (ecosystem), L4 (protocol)

---

## Part 1: Reused Mind Protocol Types

These types are used AS-IS from Mind Protocol (no changes needed).

### Node Types

**U4_Code_Artifact** (Mind Protocol)
- **Usage:** Source files (Python, TypeScript, Go, etc.)
- **Created by:** Kai (Chief Engineer)
- **Required fields:**
  - `commit` (string) - Git commit hash
  - `hash` (string) - File content hash
  - `lang` (enum) - py, ts, js, sql, bash, rust, go, other
  - `path` (string) - File path relative to repo root
  - `repo` (string) - Repository identifier
- **Example:**
  ```cypher
  CREATE (f:U4_Code_Artifact {
    name: "auth_service.py",
    description: "Authentication service implementation",
    path: "src/services/auth_service.py",
    lang: "py",
    repo: "github.com/acme/backend",
    commit: "abc123def456",
    hash: "sha256:...",
    level: "L2",
    scope_ref: "client_acme_corp",
    created_at: timestamp(),
    updated_at: timestamp(),
    valid_from: timestamp(),
    valid_to: null,
    visibility: "private",
    created_by: "kai_graphcare",
    substrate: "external_system"
  })
  ```

**U4_Knowledge_Object** (Mind Protocol)
- **Usage:** ADRs, specs, runbooks, guides, API docs
- **Created by:** Quinn (semantic extraction), Sage (documentation generation)
- **Required fields:**
  - `ko_id` (string) - Unique identifier
  - `ko_type` (enum) - adr, spec, runbook, guide, reference, policy_summary
  - `level` (enum) - L2
  - `scope_ref` (string) - Client org ID
  - `uri` (string) - Location (file path, URL, or generated://...)
- **Example:**
  ```cypher
  CREATE (doc:U4_Knowledge_Object {
    name: "ADR-015: Use PostgreSQL for Primary Datastore",
    description: "Architectural decision to use PostgreSQL instead of MongoDB",
    ko_id: "adr_015_postgresql",
    ko_type: "adr",
    uri: "docs/adr/015-postgresql.md",
    level: "L2",
    scope_ref: "client_acme_corp",
    status: "active",
    created_at: timestamp(),
    updated_at: timestamp(),
    valid_from: timestamp(),
    valid_to: null,
    visibility: "private",
    created_by: "quinn_graphcare",
    substrate: "external_system"
  })
  ```

**U4_Decision** (Mind Protocol)
- **Usage:** Decision records (what was decided, who, why, when)
- **Created by:** Nora (inferred from docs/code), Quinn (extracted from ADRs)
- **Required fields:**
  - `choice` (string) - What was decided
  - `decider_ref` (string) - Who decided (agent ID or team)
  - `level` (enum) - L2
  - `rationale` (string) - Why this decision
  - `scope_ref` (string) - Client org ID

**U4_Metric** (Mind Protocol)
- **Usage:** Metric definitions (coverage, complexity, security score)
- **Created by:** Vera (test coverage), Marcus (security metrics), Nora (architectural complexity)
- **Required fields:**
  - `definition` (string) - What this metric measures
  - `level` (enum) - L2
  - `scope_ref` (string) - Client org ID
  - `unit` (string) - Measurement unit (%, count, score, etc.)

**U4_Measurement** (Mind Protocol)
- **Usage:** Concrete datapoints for metrics (coverage = 87%, complexity = 12)
- **Created by:** Vera, Marcus, Nora (when running analysis)
- **Required fields:**
  - `metric_ref` (string) - Which metric this measures
  - `timestamp` (datetime) - When measured
  - `value` (float) - Measurement value
  - **Links to:** `U4_Metric` via `U4_MEASURES`

**U4_Assessment** (Mind Protocol)
- **Usage:** Security/compliance evaluations
- **Created by:** Marcus (Chief Auditor)
- **Required fields:**
  - `assessor_ref` (string) - Who assessed (marcus_graphcare)
  - `domain` (enum) - security, compliance, performance
  - `level` (enum) - L2
  - `scope_ref` (string) - Client org ID
  - `score` (float) - Assessment score

**U4_Agent** (Mind Protocol)
- **Usage:** Code authors, maintainers, teams, orgs
- **Created by:** Kai (extracted from Git history), Quinn (extracted from docs)
- **Required fields:**
  - `agent_type` (enum) - human, org, external_system
  - `level` (enum) - L2
  - `scope_ref` (string) - Client org ID

**U4_Work_Item** (Mind Protocol)
- **Usage:** Tasks, bugs, milestones, tickets
- **Created by:** Quinn (extracted from issue trackers), Nora (identified gaps)
- **Required fields:**
  - `level` (enum) - L2
  - `priority` (enum) - critical, high, medium, low
  - `scope_ref` (string) - Client org ID
  - `state` (enum) - todo, doing, blocked, done, canceled
  - `work_type` (enum) - task, milestone, bug, ticket, mission

**U4_Event** (Mind Protocol)
- **Usage:** Build events, deploy events, incidents, healthchecks
- **Created by:** Kai (extracted from CI/CD logs), Marcus (security incidents)
- **Required fields:**
  - `actor_ref` (string) - Who/what triggered event
  - `event_kind` (enum) - incident, publish, trade, governance, healthcheck
  - `level` (enum) - L2
  - `scope_ref` (string) - Client org ID
  - `timestamp` (datetime) - When event occurred

**U4_Goal** (Mind Protocol)
- **Usage:** Project goals, roadmap items
- **Created by:** Quinn (extracted from docs), Nora (inferred from architecture)
- **Required fields:**
  - `horizon` (enum) - daily, weekly, monthly, quarterly, annual, multi_year
  - `level` (enum) - L2
  - `scope_ref` (string) - Client org ID

---

## Part 2: GraphCare-Specific Node Types

These types are NEW for GraphCare (not in Mind Protocol).

### GC_Function

**Purpose:** Individual function/method in codebase (more granular than Code_Artifact)

**Created by:** Kai (Chief Engineer) via AST parsing

**Type-Specific Required Fields:**
- `name` (string) - Function name
- `signature` (string) - Full function signature (params, return type)
- `file_ref` (string) - Node ID of parent U4_Code_Artifact
- `line_start` (integer) - Starting line number
- `line_end` (integer) - Ending line number

**Type-Specific Optional Fields:**
- `complexity_score` (float) - Cyclomatic complexity
- `docstring` (string) - Function documentation
- `is_public` (boolean) - Exported/public vs internal
- `is_async` (boolean) - Async function?
- `is_test` (boolean) - Is this a test function?
- `return_type` (string) - Return type annotation
- `params` (array) - Parameter list with types

**Universal Attributes** (inherited):
- `description` (string) - REQUIRED - Short summary of what function does
- `level` (enum) - REQUIRED - Always "L2"
- `scope_ref` (string) - REQUIRED - Client org ID
- `created_at`, `updated_at`, `valid_from`, `valid_to` - Bitemporal tracking
- `visibility`, `created_by`, `substrate` - Privacy & provenance

**Example:**
```cypher
CREATE (fn:GC_Function {
  name: "validate_jwt_token",
  description: "Validates JWT token and returns decoded claims",
  signature: "validate_jwt_token(token: str, secret: str) -> dict",
  file_ref: "code_artifact:auth_service_py",
  line_start: 45,
  line_end: 67,
  complexity_score: 4.0,
  docstring: "Validates JWT token using RS256 algorithm. Returns claims if valid, raises AuthError if invalid.",
  is_public: true,
  is_async: false,
  is_test: false,
  return_type: "dict",
  params: ["token:str", "secret:str"],
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
})
```

---

### GC_Class

**Purpose:** Class/interface/type definition in codebase

**Created by:** Kai (Chief Engineer) via AST parsing

**Type-Specific Required Fields:**
- `name` (string) - Class name
- `file_ref` (string) - Node ID of parent U4_Code_Artifact
- `line_start` (integer) - Starting line number
- `line_end` (integer) - Ending line number

**Type-Specific Optional Fields:**
- `class_type` (enum) - class, interface, abstract_class, enum, protocol, type_alias
- `docstring` (string) - Class documentation
- `is_public` (boolean) - Exported/public vs internal
- `methods` (array) - List of method names (detailed via GC_Function nodes)
- `properties` (array) - List of properties/attributes
- `parent_classes` (array) - Base classes/interfaces (detailed via GC_INHERITS links)

**Example:**
```cypher
CREATE (cls:GC_Class {
  name: "AuthService",
  description: "Service class for handling authentication operations",
  file_ref: "code_artifact:auth_service_py",
  line_start: 15,
  line_end: 120,
  class_type: "class",
  docstring: "Handles user authentication via JWT tokens and OAuth",
  is_public: true,
  methods: ["validate_jwt_token", "refresh_token", "logout"],
  properties: ["secret_key", "token_expiry", "oauth_client"],
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
})
```

---

### GC_Module

**Purpose:** Module/package/namespace (logical grouping of code)

**Created by:** Kai (Chief Engineer) from file structure + imports

**Type-Specific Required Fields:**
- `name` (string) - Module name
- `module_path` (string) - Full module path (e.g., "src.services.auth")

**Type-Specific Optional Fields:**
- `module_type` (enum) - package, module, namespace
- `exports` (array) - Public exports (functions, classes exported)
- `file_count` (integer) - Number of files in module
- `line_count` (integer) - Total lines of code

**Example:**
```cypher
CREATE (mod:GC_Module {
  name: "auth",
  description: "Authentication module containing JWT and OAuth logic",
  module_path: "src.services.auth",
  module_type: "package",
  exports: ["AuthService", "validate_jwt_token", "JWTError"],
  file_count: 5,
  line_count: 847,
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
})
```

---

### GC_API_Endpoint

**Purpose:** REST/GraphQL/gRPC API endpoint exposed by service

**Created by:** Kai (Chief Engineer) from code analysis (route decorators, GraphQL schema)

**Type-Specific Required Fields:**
- `name` (string) - Endpoint name
- `method` (enum) - GET, POST, PUT, DELETE, PATCH, GRAPHQL, GRPC
- `path` (string) - URL path (e.g., "/api/v1/auth/login")

**Type-Specific Optional Fields:**
- `handler_ref` (string) - Node ID of GC_Function that handles this endpoint
- `request_schema` (string) - JSON schema or type definition for request
- `response_schema` (string) - JSON schema or type definition for response
- `auth_required` (boolean) - Requires authentication?
- `rate_limit` (string) - Rate limiting policy (e.g., "100/hour")

**Example:**
```cypher
CREATE (api:GC_API_Endpoint {
  name: "POST /api/v1/auth/login",
  description: "User login endpoint that returns JWT token",
  method: "POST",
  path: "/api/v1/auth/login",
  handler_ref: "function:login_handler",
  request_schema: "{email:string, password:string}",
  response_schema: "{token:string, expires_at:datetime, user_id:string}",
  auth_required: false,
  rate_limit: "10/minute per IP",
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
})
```

---

### GC_Behavior_Spec

**Purpose:** Specification of what SHOULD happen (pre/post conditions, success criteria)

**Created by:** Nora (Chief Architect) from docs + code + inference

**Type-Specific Required Fields:**
- `name` (string) - Behavior name (e.g., "User login flow")

**Type-Specific Optional Fields:**
- `pre_conditions` (array) - What must be true before
- `post_conditions` (array) - What will be true after
- `success_criteria` (array) - How we know it worked
- `failure_modes` (array) - What can go wrong
- `coverage` (enum) - full, partial, none (do implementations exist?)

**Example:**
```cypher
CREATE (spec:GC_Behavior_Spec {
  name: "User Authentication Flow",
  description: "User submits credentials, receives JWT token if valid",
  pre_conditions: [
    "User exists in database",
    "Password is hashed with bcrypt",
    "Email is validated format"
  ],
  post_conditions: [
    "JWT token issued with 1-hour expiry",
    "Login event logged",
    "User session created"
  ],
  success_criteria: [
    "Returns 200 with token on valid credentials",
    "Returns 401 on invalid credentials",
    "Returns 429 on rate limit exceeded"
  ],
  failure_modes: [
    "Database connection fails → 503 Service Unavailable",
    "Invalid email format → 400 Bad Request"
  ],
  coverage: "partial",
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "nora_graphcare",
  substrate: "organizational"
})
```

---

### GC_Architecture_Component

**Purpose:** Service/layer/boundary/subsystem in inferred architecture

**Created by:** Nora (Chief Architect) from code structure + data flows

**Type-Specific Required Fields:**
- `name` (string) - Component name (e.g., "Authentication Service")
- `component_type` (enum) - service, layer, module, subsystem, boundary

**Type-Specific Optional Fields:**
- `responsibilities` (array) - What this component does
- `interfaces` (array) - Exposed interfaces (APIs, events, functions)
- `dependencies` (array) - What this depends on (detailed via U4_DEPENDS_ON links)
- `technology_stack` (array) - Technologies used (FastAPI, PostgreSQL, Redis, etc.)

**Example:**
```cypher
CREATE (comp:GC_Architecture_Component {
  name: "Authentication Service",
  description: "Handles all user authentication and authorization",
  component_type: "service",
  responsibilities: [
    "Validate user credentials",
    "Issue and verify JWT tokens",
    "Manage user sessions",
    "Integrate with OAuth providers"
  ],
  interfaces: [
    "POST /api/v1/auth/login",
    "POST /api/v1/auth/logout",
    "GET /api/v1/auth/verify"
  ],
  technology_stack: ["FastAPI", "PostgreSQL", "Redis", "JWT"],
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "nora_graphcare",
  substrate: "organizational"
})
```

---

### GC_Test_Case

**Purpose:** Individual test (more granular than U4_Work_Item)

**Created by:** Vera (Chief Validator) from test file analysis

**Type-Specific Required Fields:**
- `name` (string) - Test name (e.g., "test_login_with_valid_credentials")
- `test_type` (enum) - unit, integration, e2e, performance, security

**Type-Specific Optional Fields:**
- `file_ref` (string) - Node ID of test file (U4_Code_Artifact)
- `line_start` (integer) - Starting line number
- `line_end` (integer) - Ending line number
- `target_ref` (string) - Node ID of what's being tested (GC_Function, GC_Class, GC_Behavior_Spec)
- `last_run_status` (enum) - pass, fail, skipped, error
- `last_run_ts` (datetime) - When last executed
- `assertions` (array) - List of assertions in test

**Example:**
```cypher
CREATE (test:GC_Test_Case {
  name: "test_login_with_valid_credentials",
  description: "Tests that valid credentials return JWT token",
  test_type: "integration",
  file_ref: "code_artifact:test_auth_py",
  line_start: 25,
  line_end: 45,
  target_ref: "behavior_spec:user_authentication_flow",
  last_run_status: "pass",
  last_run_ts: timestamp(),
  assertions: [
    "Response status code is 200",
    "Response contains 'token' field",
    "Token is valid JWT format"
  ],
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "vera_graphcare",
  substrate: "external_system"
})
```

---

### GC_Semantic_Cluster

**Purpose:** Topic/theme cluster from semantic analysis (Quinn's semantic map)

**Created by:** Quinn (Chief Cartographer) from corpus embedding + clustering

**Type-Specific Required Fields:**
- `name` (string) - Cluster theme (e.g., "Authentication System")
- `coherence` (float) - Mean pairwise similarity of cluster members (0-1)

**Type-Specific Optional Fields:**
- `centroid_embedding` (array) - 768-dim cluster center (for similarity queries)
- `document_count` (integer) - Number of documents in cluster
- `top_terms` (array) - Top representative terms/keywords
- `cluster_type` (enum) - semantic, functional, temporal

**Example:**
```cypher
CREATE (cluster:GC_Semantic_Cluster {
  name: "Authentication System",
  description: "Documents and code related to user authentication",
  coherence: 0.72,
  centroid_embedding: [0.042, -0.315, ...],  // 768 dims
  document_count: 23,
  top_terms: ["jwt", "login", "oauth", "token", "credentials", "session"],
  cluster_type: "semantic",
  level: "L2",
  scope_ref: "client_acme_corp",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "quinn_graphcare",
  substrate: "organizational"
})
```

---

## Part 3: Link Types

### Reused Mind Protocol Links (AS-IS)

**U4_IMPLEMENTS** - Code artifact implements spec/policy/capability
- Example: `(code_artifact)-[:U4_IMPLEMENTS]->(behavior_spec)`

**U4_DOCUMENTS** - Knowledge object documents code/policy
- Example: `(knowledge_object)-[:U4_DOCUMENTS]->(architecture_component)`

**U4_DEPENDS_ON** - Dependency relationship (runtime, build, logical)
- Example: `(module_a)-[:U4_DEPENDS_ON {dependency_type: "runtime"}]->(module_b)`

**U4_TESTS** - Test covers code/policy/capability
- Example: `(test_case)-[:U4_TESTS]->(function)`

**U4_REFERENCES** - Citation/dependency/inspiration
- Example: `(doc)-[:U4_REFERENCES {reference_type: "citation", uri: "..."}]->(external_doc)`

**U4_ASSIGNED_TO** - Work item ownership
- Example: `(work_item)-[:U4_ASSIGNED_TO]->(agent)`

**U4_BLOCKED_BY** - Dependency blocker
- Example: `(work_item_a)-[:U4_BLOCKED_BY {blocking_reason: "...", severity: "absolute"}]->(work_item_b)`

**U4_EMITS** / **U4_CONSUMES** - Event topology
- Example: `(service)-[:U4_EMITS]->(event_schema)`, `(service)-[:U4_CONSUMES]->(event_schema)`

**U4_CONTROLS** - Mechanism controls metric
- Example: `(architecture_component)-[:U4_CONTROLS {control_type: "regulates"}]->(metric)`

**U4_MEASURES** - Measurement measures metric
- Example: `(measurement)-[:U4_MEASURES]->(metric)`

**U4_EVIDENCED_BY** - Claim supported by proof
- Example: `(behavior_spec)-[:U4_EVIDENCED_BY {evidence_type: "document"}]->(knowledge_object)`

**U4_MEMBER_OF** - Child → Parent composition
- Example: `(function)-[:U4_MEMBER_OF {membership_type: "structural", role: "method"}]->(class)`

---

### GraphCare-Specific Link Types

**GC_CALLS** - Function A calls Function B

**Type-Specific Required Fields:**
- `call_type` (enum) - direct, async, callback, recursive
- `call_frequency` (enum) - always, conditional, rare (from static analysis)

**Example:**
```cypher
CREATE (fn_a)-[:GC_CALLS {
  call_type: "direct",
  call_frequency: "always",
  goal: "Validation logic requires token verification",
  confidence: 1.0,
  energy: 0.8,
  forming_mindstate: "code_analysis_phase",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
}]->(fn_b)
```

---

**GC_IMPORTS** - Module A imports Module B

**Type-Specific Required Fields:**
- `import_type` (enum) - full_module, specific_names, wildcard, relative

**Type-Specific Optional Fields:**
- `imported_names` (array) - Specific names imported (if not full module)

**Example:**
```cypher
CREATE (mod_a)-[:GC_IMPORTS {
  import_type: "specific_names",
  imported_names: ["validate_jwt_token", "JWTError"],
  goal: "Authentication module needed for user validation",
  confidence: 1.0,
  energy: 0.7,
  forming_mindstate: "import_analysis",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
}]->(mod_b)
```

---

**GC_INHERITS** - Class A extends/implements Class B

**Type-Specific Required Fields:**
- `inheritance_type` (enum) - extends, implements, mixin, protocol

**Example:**
```cypher
CREATE (class_a)-[:GC_INHERITS {
  inheritance_type: "extends",
  goal: "Inherit base authentication logic",
  confidence: 1.0,
  energy: 0.8,
  forming_mindstate: "class_hierarchy_analysis",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "kai_graphcare",
  substrate: "external_system"
}]->(class_b)
```

---

**GC_EXPOSES** - Component exposes API endpoint

**Type-Specific Optional Fields:**
- `exposure_type` (enum) - public, internal, partner

**Example:**
```cypher
CREATE (component)-[:GC_EXPOSES {
  exposure_type: "public",
  goal: "Provide external authentication API",
  confidence: 1.0,
  energy: 0.9,
  forming_mindstate: "api_mapping",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "nora_graphcare",
  substrate: "organizational"
}]->(api_endpoint)
```

---

**GC_SPECIFIES** - Behavior_Spec specifies Function/Class/Component

**Type-Specific Required Fields:**
- `specification_coverage` (enum) - complete, partial, minimal

**Example:**
```cypher
CREATE (behavior_spec)-[:GC_SPECIFIES {
  specification_coverage: "partial",
  goal: "Document expected authentication behavior",
  confidence: 0.85,
  energy: 0.7,
  forming_mindstate: "behavior_extraction",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "nora_graphcare",
  substrate: "organizational"
}]->(function)
```

---

**GC_VALIDATES** - Test_Case validates Behavior_Spec

**Type-Specific Required Fields:**
- `validation_coverage` (enum) - complete, partial, none

**Type-Specific Optional Fields:**
- `validated_criteria` (array) - Which success criteria are covered

**Example:**
```cypher
CREATE (test_case)-[:GC_VALIDATES {
  validation_coverage: "partial",
  validated_criteria: [
    "Returns 200 with token on valid credentials",
    "Returns 401 on invalid credentials"
  ],
  goal: "Verify authentication behavior matches spec",
  confidence: 0.9,
  energy: 0.8,
  forming_mindstate: "test_coverage_analysis",
  created_at: timestamp(),
  updated_at: timestamp(),
  valid_from: timestamp(),
  valid_to: null,
  visibility: "private",
  created_by: "vera_graphcare",
  substrate: "external_system"
}]->(behavior_spec)
```

---

## Part 4: Citizen Handoff Contracts

### Quinn (Semantic Cartographer) → Kai (Code Engineer)

**Quinn creates:**
- `GC_Semantic_Cluster` - Topic/theme clusters from corpus
- `U4_Knowledge_Object` - Extracted docs (ADRs, guides, specs)
- Links: `(cluster)-[:U4_MEMBER_OF]->(knowledge_object)` - Cluster membership

**Handoff output:**
```typescript
interface QuinnOutput {
  clusters: Array<{
    node_id: string;              // GC_Semantic_Cluster node ID
    theme: string;                // e.g., "Authentication System"
    coherence: number;            // 0-1
    document_count: number;
    top_terms: string[];
  }>;

  knowledge_objects: Array<{
    node_id: string;              // U4_Knowledge_Object node ID
    name: string;
    ko_type: "adr" | "spec" | "runbook" | "guide" | "reference";
    uri: string;
    cluster_id: string;           // Which cluster it belongs to
  }>;

  coverage_gaps: Array<{
    area: string;                 // e.g., "Payment processing"
    evidence: string;             // Why we think this exists
    severity: "high" | "medium" | "low";
  }>;
}
```

**Kai uses:**
- Clusters guide code analysis (focus on documented areas first)
- Knowledge objects link to code via `U4_IMPLEMENTS`
- Coverage gaps identify code that may lack documentation

---

### Kai (Code Engineer) → Nora (Architect)

**Kai creates:**
- `U4_Code_Artifact` - Source files
- `GC_Function` - Functions/methods
- `GC_Class` - Classes/interfaces
- `GC_Module` - Modules/packages
- `GC_API_Endpoint` - API endpoints
- Links: `GC_CALLS`, `GC_IMPORTS`, `GC_INHERITS`, `U4_MEMBER_OF`

**Handoff output:**
```typescript
interface KaiOutput {
  code_artifacts: Array<{
    node_id: string;              // U4_Code_Artifact node ID
    path: string;
    lang: string;
    line_count: number;
  }>;

  functions: Array<{
    node_id: string;              // GC_Function node ID
    name: string;
    signature: string;
    file_ref: string;             // Parent file node ID
    complexity_score: number;
    is_public: boolean;
  }>;

  classes: Array<{
    node_id: string;              // GC_Class node ID
    name: string;
    file_ref: string;
    methods: string[];            // Function node IDs
  }>;

  modules: Array<{
    node_id: string;              // GC_Module node ID
    name: string;
    module_path: string;
    exports: string[];
    file_count: number;
  }>;

  api_endpoints: Array<{
    node_id: string;              // GC_API_Endpoint node ID
    method: string;
    path: string;
    handler_ref: string;          // Function node ID
  }>;

  call_graph: Array<{
    caller_id: string;            // GC_Function node ID
    callee_id: string;            // GC_Function node ID
    call_type: "direct" | "async" | "callback";
  }>;

  import_graph: Array<{
    importer_id: string;          // GC_Module node ID
    imported_id: string;          // GC_Module node ID
    import_type: string;
  }>;
}
```

**Nora uses:**
- Code structure infers architecture (services, layers, boundaries)
- Call graphs reveal data flows
- Import graphs reveal dependencies
- API endpoints reveal public interfaces

---

### Nora (Architect) → Vera (Validator) + Marcus (Auditor) + Sage (Documenter)

**Nora creates:**
- `GC_Behavior_Spec` - What should happen (pre/post conditions, success criteria)
- `GC_Architecture_Component` - Services, layers, subsystems
- `U4_Decision` - Inferred/extracted architectural decisions
- Links: `GC_SPECIFIES`, `GC_EXPOSES`, `U4_IMPLEMENTS`, `U4_DOCUMENTS`

**Handoff output:**
```typescript
interface NoraOutput {
  behavior_specs: Array<{
    node_id: string;              // GC_Behavior_Spec node ID
    name: string;
    pre_conditions: string[];
    post_conditions: string[];
    success_criteria: string[];
    coverage: "full" | "partial" | "none";
    mechanism_refs: string[];     // Function/Class node IDs that implement
  }>;

  architecture_components: Array<{
    node_id: string;              // GC_Architecture_Component node ID
    name: string;
    component_type: "service" | "layer" | "module" | "subsystem";
    responsibilities: string[];
    interfaces: string[];         // API endpoint node IDs
    dependencies: string[];       // Component node IDs
  }>;

  decisions: Array<{
    node_id: string;              // U4_Decision node ID
    choice: string;
    rationale: string;
    decider_ref: string;
    status: "active" | "superseded";
  }>;

  gaps: Array<{
    gap_type: "missing_spec" | "missing_implementation" | "ambiguous_interface";
    description: string;
    affected_refs: string[];      // Node IDs affected
    priority: "critical" | "high" | "medium" | "low";
  }>;
}
```

**Vera uses:**
- Behavior specs define what to validate
- Success criteria become test assertions
- Coverage status guides testing priorities

**Marcus uses:**
- Architecture components reveal attack surface
- Behavior specs define security requirements
- Gaps highlight unverified security assumptions

**Sage uses:**
- Architecture diagrams visualize components
- Behavior specs populate API documentation
- Decisions become ADR documentation

---

## Part 5: Schema Migration Strategy

### Migration Script Structure

```python
"""
GraphCare Schema Migration - v1.0.0

Applies GraphCare schema to FalkorDB:
1. Create type indexes (for efficient type queries)
2. Create constraint indexes (unique IDs)
3. Validate universal attributes (all nodes/links have required fields)
"""

from falkordb import FalkorDB

def migrate_schema(graph_id: str):
    """Apply GraphCare schema to graph"""

    db = FalkorDB(host='localhost', port=6379)
    graph = db.select_graph(graph_id)

    # Create type indexes for efficient type-based queries
    node_types = [
        # Reused Mind Protocol types
        "U4_Code_Artifact", "U4_Knowledge_Object", "U4_Decision",
        "U4_Metric", "U4_Measurement", "U4_Assessment", "U4_Agent",
        "U4_Work_Item", "U4_Event", "U4_Goal",

        # GraphCare-specific types
        "GC_Function", "GC_Class", "GC_Module", "GC_API_Endpoint",
        "GC_Behavior_Spec", "GC_Architecture_Component",
        "GC_Test_Case", "GC_Semantic_Cluster"
    ]

    for node_type in node_types:
        # Create index on type_name for fast type queries
        graph.query(f"CREATE INDEX FOR (n:{node_type}) ON (n.type_name)")

        # Create index on name for fast name lookups
        graph.query(f"CREATE INDEX FOR (n:{node_type}) ON (n.name)")

    # Create indexes on common query patterns
    graph.query("CREATE INDEX FOR (n:GC_Function) ON (n.file_ref)")
    graph.query("CREATE INDEX FOR (n:GC_Class) ON (n.file_ref)")
    graph.query("CREATE INDEX FOR (n:GC_API_Endpoint) ON (n.path)")
    graph.query("CREATE INDEX FOR (n) ON (n.scope_ref)")  # Filter by client
    graph.query("CREATE INDEX FOR (n) ON (n.level)")      # Filter by level

    print(f"✅ Schema migration complete for graph: {graph_id}")

    return True
```

### Schema Validation

```python
def validate_schema(graph_id: str) -> dict:
    """Validate that all nodes/links have required universal attributes"""

    db = FalkorDB(host='localhost', port=6379)
    graph = db.select_graph(graph_id)

    # Check all nodes have universal attributes
    result = graph.query("""
        MATCH (n)
        WHERE n.created_at IS NULL
           OR n.updated_at IS NULL
           OR n.valid_from IS NULL
           OR n.level IS NULL
           OR n.scope_ref IS NULL
           OR n.description IS NULL
           OR n.name IS NULL
        RETURN count(n) as invalid_count
    """).result_set

    invalid_nodes = result[0][0] if result else 0

    # Check all links have universal attributes
    result = graph.query("""
        MATCH ()-[r]->()
        WHERE r.created_at IS NULL
           OR r.updated_at IS NULL
           OR r.valid_from IS NULL
           OR r.confidence IS NULL
           OR r.energy IS NULL
           OR r.goal IS NULL
        RETURN count(r) as invalid_count
    """).result_set

    invalid_links = result[0][0] if result else 0

    return {
        "valid": invalid_nodes == 0 and invalid_links == 0,
        "invalid_nodes": invalid_nodes,
        "invalid_links": invalid_links
    }
```

---

## Part 6: Example Graph Queries

### Query 1: Find all functions that call a specific function

```cypher
MATCH (caller:GC_Function)-[:GC_CALLS]->(callee:GC_Function {name: 'validate_jwt_token'})
RETURN caller.name, caller.file_ref, caller.signature
ORDER BY caller.name
```

### Query 2: Find behavior specs without full test coverage

```cypher
MATCH (spec:GC_Behavior_Spec)
WHERE spec.coverage IN ['partial', 'none']
OPTIONAL MATCH (test:GC_Test_Case)-[:GC_VALIDATES]->(spec)
RETURN spec.name, spec.coverage, count(test) as test_count
ORDER BY test_count ASC
```

### Query 3: Find API endpoints and their handlers

```cypher
MATCH (api:GC_API_Endpoint)-[:U4_MEMBER_OF]->(comp:GC_Architecture_Component)
OPTIONAL MATCH (api)<-[:GC_EXPOSES]-(handler:GC_Function)
RETURN api.method, api.path, comp.name as service, handler.name as handler_function
ORDER BY api.path
```

### Query 4: Find orphan code (no documentation or specs)

```cypher
MATCH (fn:GC_Function)
WHERE NOT (fn)<-[:U4_DOCUMENTS]-(:U4_Knowledge_Object)
  AND NOT (fn)<-[:GC_SPECIFIES]-(:GC_Behavior_Spec)
RETURN fn.name, fn.file_ref, fn.complexity_score
ORDER BY fn.complexity_score DESC
LIMIT 20
```

### Query 5: Find architecture components and their dependencies

```cypher
MATCH (comp:GC_Architecture_Component)
OPTIONAL MATCH (comp)-[:U4_DEPENDS_ON]->(dep:GC_Architecture_Component)
RETURN comp.name, comp.component_type,
       collect(dep.name) as dependencies,
       size(collect(dep)) as dependency_count
ORDER BY dependency_count DESC
```

---

## Part 7: Schema Versioning

**Version:** 1.0.0 (initial)

**Future versions will:**
- Add new node/link types as extraction evolves
- Refine optional fields based on real extraction
- Add indexes for common query patterns
- Deprecate unused types

**Migration path:**
- Always backward-compatible (add, never remove required fields)
- Version stored in graph metadata: `(graph:GraphCare_Schema {version: "1.0.0"})`

---

## Status

**Current:** Draft
**Review needed:** Mel (coordination), Quinn (semantic), Kai (code), Vera (validation), Marcus (security), Sage (documentation)
**Approval needed:** Founder
**Next step:** Implement FalkorDB migration script

---

**END OF SCHEMA SPECIFICATION**
