# Cross-repository contracts

Check `jade.project.json`, project instructions and task links to locate the back end. If the path/repository is missing, search only within the authorized scope; ask for the identifier when there is no unambiguous match.

1. Record the repo URL/path, branch and commit actually consulted. Do not switch branches or change the user's checkout to investigate; prefer reading through Git or an authorized isolated checkout.
2. Locate OpenAPI/GraphQL/schema, routes, DTOs, controllers, authorization and relevant tests. Check whether the published contract and the implementation diverge.
3. Map method/path, authentication, permissions, input, output, nullability, enum, error, date/currency/timezone, pagination, filters, cache, retry and cancellation as the change requires.
4. Identify the front end's client, hook, query or server action. Reuse existing type generation; do not introduce casts or fake data to hide a mismatch.
5. Distinguish existence in code from availability in an environment. Check deploy/version evidence and tests in the allowed environment. An endpoint responding does not by itself prove the expected commit was deployed.
6. When the deployed version is unknown, record `deployed version not confirmed`. Do not declare a real integration approved without matching verification.
7. Missing or incompatible API: state the affected criterion, required contract, dependency and ticket/PR when known. Do not invent an owner. Implement a mock or fallback only if it is part of the scope/requirement; label it as such.

| API | Contract/commit | Environment/version | Verification | Dependency |
| --- | --- | --- | --- | --- |
| Fill with real source | File or schema and SHA | Confirmed or unknown | Evidence and state | Known ticket/PR or not identified |

Revalidate mutable information on every resume. Active testing only in a local or explicitly authorized environment, without unwanted business side effects.
