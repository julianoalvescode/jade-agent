<div align="center">

# 🪷 Jade

**A senior full-stack engineer for Claude Code — one agent, many skills, always with OpenSpec.**

Implements and reviews front end (React, Next.js, TypeScript) and back end (APIs,
data, queues) with a focus on quality, scalability, security, performance and
UI/UX — with real context from Jira, Confluence, GitHub and Figma, spec-driven by
OpenSpec, and evidence criterion by criterion.

<sub>Version 3.0.0 · Claude Code · Codex · Cursor · Copilot · Windsurf · Gemini CLI · Cline</sub>

</div>

---

## Why Jade

Jade **is not a screen generator**. She is a senior full-stack engineer who
investigates before editing, reuses what the project already has, respects the
existing stack and never declares done without evidence. A single agent
(`jade`) preloads only `jade-workflow` and `jade-openspec`, and **discovers the
other skills on demand**, according to the task impact — no subagents, no wasted
context.

> [!NOTE]
> **One agent, many skills.** Only `jade-workflow` (the core) and `jade-openspec`
> (the spec-driven flow) are preloaded. UI, Figma, back end, delivery, tests and
> security load as separate skills only when the task needs them.

## Own skills

| Skill | Role |
| --- | --- |
| **`jade-workflow`** | Operating core: pillars, start, routing and evidence-backed delivery. Preloaded. |
| **`jade-openspec`** | 🆕 Mandatory OpenSpec flow: explore, propose, apply, verify and archive with Jade's rules. Preloaded. |
| **`jade-frontend`** | Front-end engineering: UI recon, reuse, 8-point grid, web performance and UX. |
| **`jade-backend`** | 🆕 Back-end engineering: API, data and migrations, scalability, OWASP API security, performance and observability. |
| **`jade-figma-to-code`** | Coordinates Figma → code with selective reading, component reuse and token economy. |
| **`jade-backend-contract`** | Optional/lazy: validates the front ↔ back contract (endpoint, request, response, types) via `contract-first`. |
| **`jade-delivery`** | Jira, Confluence, GitHub and cross-repo contracts, without duplicate records. |
| **`frontend-quality-gate`** | Full-stack evidence gate: `PASS`/`FAIL`/`BLOCKED`/`NOT RUN`/`N/A` (name kept for compatibility). |

Plus **21 community skills** (pinned by commit in `skills-lock.json`)
complement Jade's own rules: `ui-recon`, `spacing-system`,
`contract-first`, `figma-design-to-code`, `react-hook-form`, `state-management`,
`owasp-security-check`, `systematic-debugging`, among others.

## Pillars

| Pillar | Front end | Back end |
| --- | --- | --- |
| Quality | Strict TypeScript, behavior tests, review | Project layers, unit and integration tests |
| Scalability | Reusable components, pagination, virtualization | No local state, idempotency, queues, cache, limits |
| Security | XSS, tokens, CSP, OWASP client-side | BOLA/IDOR, mass assignment, injection, SSRF, secrets |
| Performance | Web Vitals (LCP, INP, CLS), bundle, waterfalls | N+1, indexes, `EXPLAIN`, timeouts, pool |
| UI/UX | Design system, 8pt grid, states, WCAG 2.2 AA | Clear errors and correct HTTP statuses |

## 📐 Always with OpenSpec (`jade-openspec`)

Every Jade invocation runs inside [OpenSpec](https://github.com/Fission-AI/OpenSpec).
OpenSpec defines **what** to build; Jade's skills define **how**.

| OpenSpec phase | What Jade does |
| --- | --- |
| explore | Investigates the repo and compares options on the five pillars; no code |
| propose | Writes `proposal.md`, delta specs, `design.md` (with one line per pillar) and `tasks.md` |
| apply | Implements tasks in order with the right skills; ticks a task only with evidence |
| verify | Runs `frontend-quality-gate` against every requirement and scenario |
| sync / archive | Only after the gate is `READY` and the user agrees |

Questions and reviews use explore. Any code change, even a small fix, gets a
change. If `openspec/` is missing and the CLI exists, Jade runs `openspec init`.
If the CLI is missing, Jade asks you to install it
(`npm install -g @fission-ai/openspec@latest`) and writes the artifacts by hand
in the same structure meanwhile. Jade does not commit `openspec/` unless the
project already versions it or you ask.

## 🎨 Figma → code (`jade-figma-to-code`)

Triggered automatically when the request includes a Figma frame, node or URL
("implement this screen", "convert this node to React", "match the UI to the
design"). It coordinates the flow without rewriting the official skills:

```
A. Discovery       → identify the exact node (requires node-id)
B. Project Mapping → ui-recon: map existing component/token
C. Extraction      → figma-design-to-code: get_design_context (1 call)
D. Implementation  → production code on the real stack + 8pt grid
E. Validation      → targeted lint/types/tests + visual comparison
F. Delivery        → evidence-backed summary and real open items
```

### Token economy in three levels

| Level | Reads | Stops when |
| --- | --- | --- |
| **1 — minimal** | stack, conventions and candidates via **symbol/name/import search** + 1 node call | enough to map |
| **2 — specific** | only the feature and node files (excerpts, not whole files) | the implementation is covered |
| **3 — expanded** | extra dependencies (subnodes, API contract) **only with proven need** | — |

Firm rules: never load the whole Figma file, one MCP call per node (reusing the
context), never reread an unchanged file, short outputs. **Never** sacrifice
correctness, security or visual fidelity for tokens.

### Stack-agnostic

Jade **detects** the framework, TS/JS, UI library, design system, styling
(Tailwind, CSS Modules, Styled Components, shadcn…), state, tests and lint — and
**the project's existing pattern beats the agent's preferences**. If a `Button`,
`Input` or `Modal` already exists, she reuses it before creating one.

## 🔌 Front ↔ back contract (`jade-backend-contract`)

An **optional** skill with **lazy loading**: loaded only when the task touches an
API boundary — a Figma screen that consumes an API, a Jira ticket with endpoints,
changes to services/requests/responses/DTOs, auth/authz, or an explicit contract
check request. It is **not** loaded for purely visual tasks (CSS, layout,
responsiveness, static components).

It coordinates the community skill [`contract-first`](https://skills.sh/affaan-m/ecc/contract-first)
(source of truth and verification) with Jade's cross-repo discovery:

1. detects the back-end repo (via `jade.project.json`, instructions, Jira/Confluence
   links and Jade's GitHub integration);
2. locates **only** the task's endpoints (route/symbol search);
3. picks the source of truth (OpenAPI, GraphQL Schema, JSON Schema; otherwise the
   real implementation, with a confidence level);
4. compares the front end's endpoint, request, response and TS types with the
   contract and **reports mismatches** — without inventing contracts. When the back
   end is in scope, `jade-backend` implements both sides.

Stacks: Java/Spring Boot, Node (Express, NestJS, Fastify), REST + OpenAPI/Swagger,
GraphQL. Back end unreachable → `BLOCKED` with the possible checks, without
simulating approval.

## Install in your project

Requirements: **Python 3.10+** and **Git**. The full install needs network access
to fetch the manifest commits; Node/npm are not needed to install Jade (only to
install the OpenSpec CLI).

```bash
# full install (own skills + 21 community skills)
bash /path/jade-agent/scripts/install-skills.sh claude-code --project /path/my-project

# only the eight own skills, no network
bash /path/jade-agent/scripts/install-skills.sh claude-code --project /path/my-project --core-only

# update while preserving differing files (backup in .jade/backups/)
bash /path/jade-agent/scripts/install-skills.sh claude-code --project /path/my-project --replace
```

The installer does **not** change `CLAUDE.md`, `AGENTS.md`, `.mcp.json` or personal
configuration: conflicts are reported before writing. It also accepts `codex`,
`cursor`, `github-copilot`, `windsurf`, `gemini-cli`, `cline` and `universal` —
those modes install into `.agents/skills` (or equivalent) and write `JADE.md`.

## Configure and use

1. Copy `jade.project.example.json` to `jade.project.json` and fill in the known repos,
   documents and environments (empty fields = unknown, not a contract).
2. Reuse the authenticated connectors — Jira/Confluence, GitHub and **Figma**. See
   [docs/connectors.md](docs/connectors.md). The MCP example has no credentials.
3. Install the OpenSpec CLI and run `openspec init` in the project (or let Jade do it).
4. Open a Claude session in the project and ask.

**Example — full ticket:**

> Use the Jade agent to implement ticket PROJ-123. Read the linked documents,
> check the back-end contract and validate the criteria. Prepare the PR
> with the evidence.

**Example — Figma → code:**

> Jade, implement this Figma screen:
> `https://www.figma.com/design/<fileKey>/Screen?node-id=12-345`.
> Reuse the project components and keep the 8-point grid.

> [!IMPORTANT]
> **Figma MCP.** If `get_design_context` is not exposed/authenticated, Jade
> records `BLOCKED` on the visual step and **does not recreate the screen from memory**.
> Connect the `figma` server (`claude mcp add --transport http figma https://mcp.figma.com/mcp`)
> and complete OAuth in `/mcp`. The entry is also in `.mcp.example.json`.

## Evidence-backed delivery

Each task links **criterion → implementation → evidence → state**, using
`PASS`, `FAIL`, `BLOCKED`, `NOT RUN` or `N/A`. Jade distinguishes implemented code,
validation, open PR, merge and deploy — and, when resuming, checks the remote
state before writing, avoiding duplicates.

## Maintenance and verification

The canonical source of the shared rules is `skills/jade-workflow/SKILL.md`. After
changing it:

```bash
python3 scripts/sync-instructions.py            # regenerates AGENTS.md, AGENT-PROMPT.md and jade.md
python3 scripts/validate.py                      # manifest, skills, references, preload and parity
python3 -m unittest discover -s tests -v         # installer and own-skill tests
```

No command needs network access. CI runs these checks
([.github/workflows/validate-agent.yml](.github/workflows/validate-agent.yml)) and
offers a full smoke test on `workflow_dispatch`. The installer only consumes
the manifest, fetches the exact SHA, checks the skill name and **does not run
third-party scripts** during installation. See [docs/validation.md](docs/validation.md) and
[docs/evaluation-scenarios.md](docs/evaluation-scenarios.md).

## Provenance

Jade's own skills and engineering rules evolve the original configuration of
`julianoalvescode/jade-agent` (base `5f9af5a777be07db7f316ca60512d8f38ff33b6d`).
Third-party skills are downloaded from the manifest repositories and commits,
keeping their files; the package does not redistribute them as its own content.
Pinning the commit guarantees traceability; it does not replace a security review.
