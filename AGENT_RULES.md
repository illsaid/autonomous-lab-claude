# Agent Rules

## Core Operating Rules

The agent may explore widely, but every run must improve the repository in a concrete way.

The agent should prefer:

- working artifacts over planning
- small prototypes over broad frameworks
- public evidence over vibes
- executable behavior over documentation-only changes
- simple experiments over grand architecture
- permissively licensed references over unlicensed code

Documentation-only changes may not happen twice in a row.

Every third run must produce or improve something executable, testable, queryable, playable, viewable, or otherwise usable.

The agent may change the project direction, but must record the reason in `DECISIONS.md`.

## Change Limits

Each run may change at most 3 files unless `AGENT_STATE.md` explicitly records why a larger atomic change is necessary.

Each run must update:

- `AGENT_STATE.md`
- `CHANGELOG.md`

Each run should add or update a machine-readable run record under `RUNS/` when practical.

## Public GitHub Research Rules

The agent may search public GitHub repositories for ideas, examples, APIs, implementation patterns, datasets, and curated repo lists.

The agent may not copy code from another repository unless all of the following are true:

1. The source repository has a detected permissive license:
   - MIT
   - Apache-2.0
   - BSD-2-Clause
   - BSD-3-Clause
   - ISC
2. The copied code is small, specific, and necessary.
3. The source is recorded in `THIRD_PARTY_NOTICES.md` with:
   - repository URL
   - file path
   - commit SHA or release version if available
   - license
   - what was copied or adapted
4. The relevant license text is copied into `/licenses/` if required.
5. The agent does not copy from repositories with:
   - no license
   - unclear license
   - GPL
   - AGPL
   - commercial/proprietary/custom license
   - archived repo unless explicitly justified

Preferred order:

1. Learn from the code and write a fresh implementation.
2. Add a maintained package dependency.
3. Adapt a small permissively licensed snippet with attribution.
4. Vendor code only if no better option exists.

The agent may not bulk-clone repositories into this project.

## External Services

The agent may not add Supabase, hosted databases, paid APIs, queues, auth systems, or external infrastructure until the project has a working local artifact.

External infrastructure may be proposed only after the agent documents:

1. the current local limitation,
2. why files are no longer sufficient,
3. the minimum schema or service needed,
4. what new capability the service enables,
5. how the project still works in degraded/local mode.

Default preference:

1. files first
2. JSONL second
3. SQLite third
4. hosted services only when clearly justified

## Anti-Fiddling Rule

Once the project has a working artifact, the agent may not make cosmetic, organizational, or documentation-only changes unless one of the following is true:

- the change helps a user run the project
- the change fixes ambiguity in the project purpose
- the change documents a real behavior that already exists
- the change is part of final packaging

After MVP exists, every run must either:

- fix a real defect
- add a user-visible capability
- improve test coverage
- improve installation/use
- prepare the final report

No endless refactors. No naming churn. No roadmap gardening.
