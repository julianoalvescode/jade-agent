---
name: frontend-quality-gate
description: Verify requirements and readiness of front-end and back-end changes with evidence from code, contract, UI, data, security, performance, tests and CI. Use for review, PR preparation, regression and completion of Jade tasks.
---

# Full-stack quality gate

The name `frontend-quality-gate` is kept for compatibility; the gate covers front end and back end.

Choose review (read-only), execution (authorized changes) or PR preparation/publication according to the request. Read the ticket and available documents, the diff and the repo instructions. Do not assume access to external systems.

## States

- `PASS`: executed or inspected with concrete evidence matching the criterion.
- `FAIL`: check executed and requirement violated.
- `BLOCKED`: access, environment, data or a decision prevents a required check.
- `NOT RUN`: relevant check not executed; explain the reason and the risk.
- `N/A`: the change does not affect the check; justify it.

Never infer PASS from the absence of errors. A build does not replace a functional test. A mock does not prove a real integration. Evidence from another commit does not prove the current diff.

## Checks by impact

| Area | Adequate evidence |
| --- | --- |
| Requirement | Criterion linked to behavior, file and test/inspection |
| Contract | Schema/code and SHA; payload, error, auth and environment |
| UI | Components/tokens, grid, states, responsiveness and rendered comparison |
| Accessibility | Relevant keyboard, focus, semantics, labels and contrast |
| UX | Loading, empty, error, success, action feedback and clear messages |
| Tests and code | Real commands, output/exit code and affected cases |
| Security | Data flow and controls at the changed boundaries; per-resource authz on the server; no secrets/PII in logs or the client |
| Performance | Evidence proportional to the changed path (Web Vitals, bundle, `EXPLAIN`, query count); no invented metrics |
| Scalability | Pagination, limits, idempotency, cache with invalidation and no fragile local state |
| Data | Reversible and compatible migration, constraints, indexes and short transactions |
| Operations | Structured logs without sensitive data, generic errors to the client and a rollback plan |
| CI and delivery | Run on the correct commit, required checks/reviews, conflicts and real state |
| Documentation | Changed decision or behavior reflected when authorized |

Start with inspection and focused tests; widen according to risk and the repo's real gates. Do not change dependencies/lockfiles/configuration just to get green. Distinguish introduced failure, demonstrated pre-existing failure and unknown origin.

After editing code or receiving a new commit, rerun the affected checks. For UI, do not present static inspection as browser validation.

## Result

Use `READY` only when the required criteria/gates are satisfied; `READY WITH CAVEATS` for explained non-blocking residual limitations; `NOT READY` when a required criterion/gate fails or is blocked/not validated. An optional check not executed does not automatically block a low-risk change.

Deliver findings by severity, location, impact and fix, followed by a `criterion → implementation → evidence → state` matrix. Report commands, limitations, remaining QA and external actions taken/proposed. Do not confuse technical readiness with authorization to merge or publish.
