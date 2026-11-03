---
name: jade-frontend
description: Implement and review React, Next.js and TypeScript front end while preserving components, contracts, security and tests. Use for code changes, UI, Figma, forms, state and diagnosis in Jade's flow.
---

# Front-end engineering

Read [engineering.md](references/engineering.md) section by section according to impact. That reference holds Jade's original rules. Do not run the visual routine when no UI is affected.

## Routing

| Impact | Reference sections | Complementary community skills, if installed |
| --- | --- | --- |
| Any implementation | Understand repo, business, slices, implement, validate and review | domain-modeling, typescript-quality, code-review-and-quality, verification-before-completion |
| UI | UI recon, reuse-first, visual contract and 8-point grid | ui-recon, spacing-system, frontend-design, web-design-guidelines |
| Figma | Figma → code flow, assets and rendered comparison | jade-figma-to-code (coordinates figma-design-to-code) |
| React/Next | Implementation, SSR/RSC, web performance and UX | vercel-react-best-practices, vercel-composition-patterns |
| API | Analyze back end and data boundaries | jade-backend-contract (coordinates contract-first), api-and-interface-design |
| Back end in scope | — | jade-backend |
| Tests | Test behavior and validate the project | javascript-testing-patterns, webapp-testing |
| Security | Review proportional to risk; full review for auth, data or critical boundaries | owasp-security-check |
| Bug | Diagnosis and regression | systematic-debugging |
| E2E | Only when an existing tool or the scope justifies it | playwright-best-practices |
| State/form | Only with existing libraries | state-management (TanStack Query v5/Zustand v5), react-hook-form |
| TDD | Only on explicit request or agreed boundary | tdd |

Load only the relevant skills. The reference's own instructions remain valid in a `--core-only` install; if a complementary skill is not installed, report its absence when relevant without claiming it ran.

## Core rules

- Investigate and compose existing components. Preserve tokens, fonts and public APIs.
- UI requires the 8-point grid; 4 px only for justified micro-spacing, 1–2 px for border/divider/optical correction. Accessibility takes priority. A conflict with Figma/tokens must be identified and resolved in the smallest scope, without a broad refactor.
- Read the node's design context before implementing Figma. Discover the tool's real schema; use `skillNames` only if the exposed schema accepts it. Do not send assumed parameters. Without the needed context, block only the dependent visual implementation.
- Do not invent contracts; compare back-end code and environment availability with `jade-delivery`.
- Test behavior with the existing runner and run checks proportional to risk. Do not create low-value tests just to tick a checklist, or install tools outside the scope.
- Review security at the changed boundaries. Real authorization belongs to the server. Do not expose secrets or extend active testing to production without authorization.
- Fix introduced failures and present evidence through `frontend-quality-gate`.
