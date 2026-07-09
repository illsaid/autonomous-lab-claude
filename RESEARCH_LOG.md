# Research Log

Research entries should use this format:

```md
## Research entry

Date:
Goal:
Search query:
Repos inspected:
Useful patterns:
License status:
Decision:
Copied code: yes/no
Attribution needed: yes/no
Next action:
```

The agent may research public GitHub repositories, curated lists, datasets, documentation, and examples. Research should lead toward concrete artifacts, not endless cataloging.

## Research entry

Date: 2026-07-09
Goal: Ground SEED.md's "Forgotten Workshop" premise in real public data before building anything, and identify a concrete first artifact direction.
Search query: web search "curated list abandoned unmaintained but interesting github repositories awesome"; GitHub Search API query `archived:true stars:50..500 pushed:<2021-01-01`
Repos inspected: mozilla/notes, sorentwo/readthis, danimahardhika/candybar-library, kanjielu/jeeves, jacobian/django-deployment-workshop (live metadata captured via GitHub Search API on 2026-07-09)
Useful patterns: (a) no existing curated "awesome list" specifically indexes abandoned-but-interesting repos — the space SEED.md describes is real and unfilled by existing awesome-list tooling, which mostly indexes actively maintained projects; (b) GitHub's Search API directly supports the qualifiers a discovery tool needs (`archived:true`, `pushed:<date>`, `stars:<range>`), so this doesn't require any third-party infra, just the public API; (c) within this sandbox, `api.github.com` is reachable through the agent's own fetch tool but NOT through subprocess/bash network calls (proxy-blocked) — recorded in AGENT_STATE.md so future runs don't ship a network-calling script they can't actually test in-sandbox, even though such a script would work fine for a normal user with direct internet access.
License status: All 5 seeded candidates are cataloged as metadata only (name/url/description/license/topics) — no code copied or vendored from any of them, so THIRD_PARTY_NOTICES.md is unchanged. mozilla/notes carries MPL-2.0 (not on AGENT_RULES.md's copy-allowed list) but is only referenced/cataloged, never copied from.
Decision: Build a small local-first CLI (`workshop.py`) over a curated JSONL dataset (`data/candidates.jsonl`) rather than a live-fetching tool, so the first artifact is fully executable and testable with zero network dependency. Live GitHub discovery becomes a research activity performed during future runs (via the agent's own tools), with results committed as curated JSONL — consistent with AGENT_RULES.md's "files first, JSONL second" preference.
Copied code: no
Attribution needed: no
Next action: Expand the dataset with more verified entries in a future run; consider a ranking heuristic in `workshop.py`; consider a short product README section once the direction proves out over a couple more runs.
