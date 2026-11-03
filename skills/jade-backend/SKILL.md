---
name: jade-backend
description: Implement and review back end (REST/GraphQL APIs, services, data, queues and jobs) with a focus on quality, scalability, security and performance. Use when the task scope includes an endpoint, controller, service, repository, migration, schema, job, queue, cache or server-to-server integration. Do NOT use just to consume an API from the front end; use jade-backend-contract for that.
---

# Back-end engineering

Read [engineering.md](references/engineering.md) section by section according to impact. Detect the real stack (Java/Spring Boot, Node with Express/NestJS/Fastify, Python, Go, .NET, etc.), its layering patterns, ORM, migrations, tests and lint. **The project's existing pattern beats the agent's preference.**

## When to use

- The request includes changing or creating server, database, queue, job or integration code.
- A full-stack task requires changing both sides of a contract.

If the back end is not in the authorized scope, do not change it: use `jade-backend-contract` to check the contract and record the dependency.

## Routing

| Impact | Reference sections | Complementary community skills, if installed |
| --- | --- | --- |
| Any change | 1 repository, 2 domain, 9 tests, 10 validation, 11 review | domain-modeling, code-review-and-quality, verification-before-completion |
| API/contract | 3 API design and compatibility | api-and-interface-design, contract-first |
| Data | 4 modeling, migrations and transactions | — |
| Scalability | 5 concurrency, idempotency, queues and cache | — |
| Security | 6 OWASP API Top 10 and secrets | owasp-security-check |
| Performance | 7 measurement, queries and budget | — |
| Operations | 8 observability and resilience | — |
| Bug | Diagnosis with proven root cause | systematic-debugging |
| TDD | Only on explicit request or agreed boundary | tdd |

Load only the relevant skills. Without the complementary skill installed, follow Jade's own reference and report the absence when relevant.

## Core rules

- Contract first: change a public API only with backward compatibility or an agreed new version. Update OpenAPI/schema and front-end types in the same scope.
- Validate every input at the boundary, authorize on the server per resource (anti-IDOR/BOLA) and never trust client data.
- Parameterized queries, no N+1, with indexes and pagination on lists. Measure before optimizing.
- Migrations are reversible, compatible with the previous running version and never applied to a shared environment without authorization.
- Repeatable operations must be idempotent; external calls use a timeout, retry with backoff and a limit.
- Structured logs with no secrets or PII; errors without stack traces for the client.
- Do not change infrastructure, permissions, shared databases or deploys without an explicit request.
- Test behavior (unit + integration at the real boundary) and present evidence through `frontend-quality-gate`.
