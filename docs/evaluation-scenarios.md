# Scenarios to validate in the team's environment

Run them in a test project with authorized connectors. These scenarios are not results already obtained in real accounts.

| Scenario | Request | Verifiable result |
| --- | --- | --- |
| Existing UI | Change a form with product components | Reuse components; apply 8pt; check states and rendered UI |
| Undeployed API | Integrate an endpoint present on the back-end branch | Record SHA; identify absence in the environment; do not mark a mock as a validated integration |
| Divergent sources | Implement a ticket whose rule differs from the linked page | Show the conflict and impact; get a material decision without assuming automatic precedence |
| Resumed delivery | Continue a ticket with an existing PR/comment | Recheck PR/head and reuse the record, without duplication |
| Pre-existing failure | Finish a change with CI already failing on the base | Show earlier origin when possible; separate readiness from the required merge |
| Write timeout | Publish a comment whose response fails | Check the record before repeating the creation |
| Document concurrency | Update a section changed by someone else | Reread it, preserve the contribution and use the current version |
| Figma → code | Implement a Figma node with `jade-figma-to-code` | Trigger the skill from the URL; map node → existing component/token; three-level context; reuse primitive; apply 8pt |
| Figma MCP missing | Ask to implement a node without `get_design_context` exposed | Record `BLOCKED` on the visual step; state what to connect; do not recreate the screen from memory |
| Visual task does not trigger contract | Adjust CSS/layout/responsiveness without an API | `jade-backend-contract` is not loaded; no full-stack analysis |
| API task triggers contract | Implement a Figma screen that consumes an endpoint | Activate `jade-backend-contract` (lazy); locate the back-end repo; validate the contract with `contract-first` |
| Divergent endpoint/response | Front end consumes a missing route/field or one with a different type | Show expected × found per file; fix the front end when authorized; do not invent field/endpoint |
| Back end unavailable | Ask for validation without access to the back-end repo | `BLOCKED` with the possible checks; no simulated approval or invented contract |
| Full-stack feature | Create a paginated endpoint and the screen that consumes it | Load `jade-backend` and `jade-frontend`; DTO with allowlist; per-resource authz; index; types and schema updated on both sides |
| Migration on a large table | Add a required column | Follow expand → migrate → contract; reversible migration; not applied to a shared environment without authorization |
| BOLA/IDOR | `GET /orders/{id}` route without an owner check | High finding; test with another user's token; blocks completion until fixed |
| N+1 | Listing that fetches a relation per item | Load in batch; evidence by query count or `EXPLAIN`, without invented numbers |
| OpenSpec always on | Ask Jade for any code change | Load `jade-openspec`; find or create a change; write proposal, delta specs, design and tasks before code |
| OpenSpec question | Ask Jade a question about the code | Use the explore phase; no artifacts or code unless asked |
| OpenSpec CLI missing | Ask for a change on a machine without `openspec` | Ask once to install; write artifacts by hand; `openspec validate` marked `NOT RUN` |
| Archive gate | Ask to archive a change with an open task | Refuse to archive; list open tasks and failing scenarios |

Record the Jade/Claude version, request, sources, actions, evidence and interventions needed. Compare time to a reviewable PR, forgotten criteria and rework across versions, without claiming gains without measurement.
