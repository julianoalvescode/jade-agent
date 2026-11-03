---
name: jade-delivery
description: Drive tasks tied to Jira, Confluence, GitHub and back-end repositories. Use to gather requirements, check cross-repo contracts, prepare PRs, follow CI or update authorized records without duplication.
---

# Integrated delivery

## 1. Establish access and scope

Discover the tools actually exposed. Do not assume names, schemas, authentication or connection just because a configuration file exists. Prefer authenticated connectors/MCP; for GitHub, use authenticated `gh` if available. Use local Git to inspect authorized repos. Record a blocker only for the dependent steps and move on with independent work.

Identify whether the request is a review, execution, PR preparation or publication/merge. Reuse explicit session authorizations; do not interpret reading a ticket as authorization to change its status or send messages.

## 2. Build minimal context

- Jira: read description, criteria, relevant comments, QA, dependencies and links; confirm which ticket is the target.
- Confluence: read linked pages and search the domain only when needed; record version/date, source and relevant excerpt.
- Front end: map flow, components, client, tests and PR conventions.
- Back end: follow [backend-contracts.md](references/backend-contracts.md).
- GitHub: locate related PRs, base/head, reviews and relevant checks.

Use [delivery-record.md](references/delivery-record.md) as a compact structure. Record verifiable sources and divergences. Resolve differences through an explicit product/engineering decision, without assuming the newest document or the code always wins. Ask one objective question only when the divergence blocks a material choice.

## 3. Implement and validate

Link each criterion to the affected flow, the implementation and the evidence. Keep API dependencies separate from authorized mocks. Load `jade-frontend`, `jade-backend` and `frontend-quality-gate` according to scope. Never mark a functional criterion as approved just because lint or build passed.

## 4. Prepare or publish

Follow [external-updates.md](references/external-updates.md) for branch, PR, Jira and Confluence. Before an authorized write, reread the record and check whether the result already exists. On a timeout, check the state before repeating the operation.

Prepare the content and evidence before requesting any authorization that is actually missing. Do not require duplicate confirmation. Update only the affected part and preserve other people's contributions.

## 5. Resume and conclude

Recheck the PR branch/head, ticket status, page version and related CI run. Invalidate evidence affected by new commits or requirement changes. Do not confuse `implemented`, `validated`, `PR open`, `merged` and `published`; confirm each state at its source.

If a local checkpoint is requested, store only sources, decisions, refs and next actions, without sensitive payloads; revalidate mutable data when resuming. Report actions taken, proposed and blocked in separate categories.
