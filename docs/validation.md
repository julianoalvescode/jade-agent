# Validation of release 3.0.0

Date: 2026-11-03. Host: Windows, Python 3.12.10.

| Check | State | Evidence |
| --- | --- | --- |
| Installer and own-skill tests | PASS | `python -m unittest discover -s tests`: 43 tests, 42 passed, 1 skipped |
| Symlink destination test | NOT RUN | Skipped on this host: Windows denies symlink creation without privilege (`WinError 1314`). Runs on Linux CI |
| Portable instruction parity | PASS | `scripts/sync-instructions.py --check` |
| Manifest, names, paths and preload | PASS | Covered by the test suite and `validate.py` checks before `bash -n` |
| Shell wrapper syntax | BLOCKED | `bash -n` unavailable: WSL has no distribution installed on this host. Runs on Linux CI |
| `jade-openspec` mandatory and preloaded | PASS | `OpenSpecSkillTests`: workflow step, agent preload, phase mapping, missing-CLI path |
| `jade-backend` and full-stack pillars | PASS | `FullStackSkillTests` |
| English-only skills and instructions | PASS | `EnglishOnlyTests` |
| Full install with community skills | NOT RUN | Not repeated for 3.0.0; the community manifest entries did not change |
| Claude and the team's real connectors | NOT RUN | User authentication and runtime unavailable in this environment |
| Clients other than Claude/Codex | NOT RUN | Directory mappings provided; loading by the client not exercised |

The installation tests do not prove the quality of all community instructions or that the connectors work. The CI workflow runs the same checks on Linux.
