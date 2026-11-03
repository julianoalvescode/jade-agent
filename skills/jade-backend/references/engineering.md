# Jade back-end engineering rules

## Navigation

- 1: repository; 2: domain; 3: API; 4: data; 5: scalability.
- 6: security; 7: performance; 8: operations; 9–11: tests, validation and review.

Read only the affected sections. External skills are complementary when
installed; without them, follow these rules and declare the checks not performed.

## 1. Understand the repository

- Read `AGENTS.md`, `CLAUDE.md`, `README`, ADRs and architecture documentation.
- Identify language, framework, build (`pom.xml`, `build.gradle`,
  `package.json`, `pyproject.toml`, `go.mod`), runtime version and lockfile.
- Map the real layers: controller/resolver → service/use case → repository →
  model; where validation, DTO mapping, error handling and auth live.
- Locate migrations, seeds, per-environment configuration, similar tests and
  the CI pipeline.
- Read only variable names and example files. Never open `.env`,
  credentials, keys or database dumps.

## 2. Model the domain

- Record actor, goal, business rule, invariants and acceptance criteria.
- Decide where each invariant is enforced: database (constraint), domain or service.
- List side effects: write, event, email, external call, audit.
- Use the domain vocabulary already present in the code.

## 3. Design the API

- Follow the existing style (REST, GraphQL, RPC), naming, response envelopes and
  error format (prefer RFC 9457 `application/problem+json` if already adopted).
- Correct methods and statuses: 200/201/204, 400 validation, 401 unauthenticated,
  403 forbidden, 404, 409 conflict, 422 business rule, 429 rate limit.
- Lists are always paginated (cursor for high volume), with filters and sorting
  validated by an allowlist and a maximum page size.
- Compatibility: adding an optional field is safe; removing, renaming or changing a
  type is a breaking change and requires a new version or a coexistence period.
- Update the OpenAPI/GraphQL schema, generated types and the front-end consumer in
  the same scope. Use `contract-first` and `api-and-interface-design` when available.
- Do not expose database entities directly: map to a DTO with only the needed fields.

## 4. Data, migrations and transactions

- Model with constraints (NOT NULL, UNIQUE, FK, CHECK) to protect invariants.
- Create indexes for new filters, joins and sorts; check the plan
  (`EXPLAIN`) on list or report queries.
- Versioned, small and reversible migrations.
  Follow expand → migrate → contract: the previous version of the application must
  keep working.
- On large tables, avoid long locks: create indexes concurrently when the
  database supports it and backfill in batches.
- Short transactions, only around the write that must be atomic. No
  external HTTP calls inside a transaction.
- Handle concurrency: optimistic locking (version) or a unique constraint instead of
  unprotected "read then write".
- Dates in UTC, money as decimal/integer cents, validated enums.
- Never run a migration, seed or data script in a shared environment without
  explicit authorization and a backup.

## 5. Scalability

- No in-memory local state between requests; session and cache in
  shared storage when there is more than one instance.
- Repeatable operations are idempotent (idempotency key on payment,
  order or integration POSTs; queue consumers tolerant of duplicate delivery).
- Slow or non-critical work goes to an async queue/job with retry, backoff,
  an attempt limit and a dead-letter queue.
- Cache only with a clear owner, key, TTL and invalidation rule. Do not cache
  per-user data in a shared cache without the identity in the key.
- Limit everything that grows: payload size, page, upload, batch, connections and
  fan-out. Apply rate limiting on public or expensive routes.
- External calls with an explicit timeout, retry only on transient errors and a
  circuit breaker when the project already has the pattern.
- Think at 10× the current volume: does the algorithm or query remain acceptable?

## 6. Security (OWASP API Security Top 10:2023 and Top 10:2025)

Risk-proportional review on every change; full review for auth, payment, PII,
upload, multi-tenant, admin or external integration. Use `owasp-security-check`.

- **Object-level authorization (BOLA/IDOR):** every resource access checks that the
  user/tenant may see or change it, on the server, on every request.
- **Function-level authorization:** admin routes and privileged actions with an
  explicit check; deny by default.
- **Mass assignment / excessive exposure:** input DTO with a field allowlist;
  output DTO without internal or sensitive fields.
- **Authentication:** use the existing mechanism; validate token signature, issuer,
  audience and expiration; passwords with a strong hash (bcrypt/argon2).
- **Injection:** parameterized queries/ORM; never concatenate SQL, shell, LDAP or
  paths with user input. Validate type, size and format at the boundary.
- **SSRF:** user-supplied URLs only with a destination allowlist; block the
  internal network and cloud metadata.
- **Upload:** validate real type, size and name; store outside the public root.
- **Secrets:** in environment variables or a vault; never in code, logs, tests or
  responses. Do not log tokens, passwords, cookies or personal documents.
- **Errors:** generic response to the client, details only in the internal log.
- **CORS and headers:** explicit origins, no `*` with credentials.
- **Dependencies:** read-only package-manager audit; do not update or run
  `audit fix` outside the scope.

Classify findings as critical, high, medium or low with evidence, category,
impact and fix. A critical or high finding introduced by the change blocks
completion. Active testing only in a local or authorized environment.

## 7. Performance

- Measure before and after on the changed path (light load test, `EXPLAIN`,
  profiler or an existing metric). Do not invent numbers.
- Eliminate N+1: load relations in batch or with a join; count queries in the test
  when the project allows.
- Select only the needed columns; paginate in the database, never in memory.
- Avoid heavy synchronous work in the request; move it to a job when it exceeds the
  agreed latency budget.
- Connection pool and timeouts consistent with the load; do not open a connection per item.
- Compression and HTTP caching (`ETag`, `Cache-Control`) when the resource allows.

## 8. Operations and observability

- Structured logs with correlation (request id/trace id) and an appropriate level.
- Metrics and traces following the existing pattern for new routes and jobs.
- Health/readiness checks must not depend on optional external services.
- Feature flag or gradual rollout for risky changes, when the project uses them.
- A clear rollback plan for code and migration.

## 9. Test behavior

- Unit tests for business rules and edge cases.
- Integration at the real boundary (controller + test database/Testcontainers, or
  the project's pattern) for route, transaction and migration.
- Security tests at the changed boundaries: no token, another user's token
  (BOLA), invalid payload, extra field (mass assignment), limit exceeded.
- Contract tests when the project has them (OpenAPI, Pact, schema snapshot).
- Mock only at the external boundary (third-party network, clock, queue).
- For regressions, reproduce the failure with a test before fixing.

## 10. Validate the project

Run, when they exist: focused tests, suite, lint/format check, typecheck or
compilation, build and a read-only dependency audit. Read output and exit code.
Fix failures caused by the change. Separate introduced failure, proven pre-existing
failure and environment blocker.

## 11. Review before delivery

Use `code-review-and-quality` on the changed files: correctness, readability,
architecture, security, scalability and performance. Fix findings caused
by the change and repeat the affected checks, without a broad refactor.

# Limits

- Do not run destructive commands, `DROP`/`TRUNCATE`, force push or hard reset.
- Do not change infrastructure, IAM, permissions, shared databases or deploys without
  an explicit request.
- Do not disable tests, lint, validation or auth checks to get green.
- Do not update dependencies or lockfiles incidentally.
