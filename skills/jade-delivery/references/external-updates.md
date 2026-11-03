# External updates and resuming

## GitHub

- Inspect local changes, conventions, base branch and existing PRs. Create a branch consistent with the ticket when the implementation requires it, without losing local work.
- Before creating an authorized PR, look for a PR with the same repo/head/base and ticket; if one exists, update it within the authorized scope.
- Preserve the repo template. Include problem, solution, ticket, criteria, real tests, contract impact, UI when applicable and open items.
- With `gh`, write the body to a temporary file and use `--body-file`; do not interpolate ticket text into the shell.
- For an authorized merge, recheck the head SHA, conflicts, approvals, CODEOWNERS and checks required by policy. Checks must match the required head/merge queue. CI from an earlier commit is not sufficient.
- Do not use bypass, `--admin`, force push or skip required checks. Confirm the merge result before announcing it.

## Jira

- Distinguish comment, field edit and status transition. Perform only the authorized action and use the transitions available in the real workflow.
- Look for a previous delivery comment by ticket and PR URL. Update only a record that is unambiguously your own; when ambiguous, do not overwrite other people's contributions.
- After a timeout, recheck the state before repeating a creation. Do not publish a duplicate because the first response did not arrive.
- Report evidence and dependencies. Do not move to done because a PR or commit exists; follow the team's definition of done.

## Confluence

- Locate the correct page and its current version. Preserve native format, macros and other people's sections.
- Prepare an update limited to the changed behavior. Use versioning/concurrency control if the tool exposes it.
- On a version conflict, reread and reapply the change on the new version. Do not overwrite the whole page from an old copy.
- Without partial editing or safe control, prepare the content for review and state the limitation instead of replacing third-party data.

## Idempotency and authorization

The logical key of a delivery combines ticket, repository and PR/head. Use identifiers returned by the tools, never invented IDs. Record confirmation of each write before moving on. Failure or lack of permission in one tool does not grant authorization in another.

Do not publish to Jira/Confluence/Slack from a generic completion hook. Messages to people or channels require explicit authorization and a verified recipient.
