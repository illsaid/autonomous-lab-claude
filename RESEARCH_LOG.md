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

## Research entry

Date: 2026-07-09
Goal: Fulfil run 2's "Next Suggested Action" -- do a live research pass and append genuinely verified new candidates to data/candidates.jsonl, satisfying the every-third-run executable/testable rule with real data rather than code alone.
Search query: web search "archived unmaintained github repository 'no longer maintained' interesting abandoned tool 2019 2020"; "PagerDuty cronner github repository archived"; "github archived abandoned game engine prototype interesting 'archived by the owner' MIT license small project"; "github archived deprecated data visualization tool 'no longer maintained' 2019"
Repos inspected: PagerDuty/cronner, CartoDB/labs-postgresql, tapio/darkcorners, mrDIMAS/DmitrysEngine (all four fetched directly via GitHub repo pages to verify real stars/license/archive-status/dates; only the first two had reliably server-rendered dates, so only those two were added this run)
Useful patterns: (a) GitHub server-renders archive-banner text ("This repository was archived by the owner on <date>"), release tags, and self-reported "last updated on <date>" text directly in the HTML, so these are reliably fetchable without JS execution; (b) the commits page (/commits/master) is client-rendered and returns empty content via a plain fetch -- not usable for verifying pushed_at without a JS-capable browser tool; (c) api.github.com and github.com remain unreachable via bash/subprocess in this sandbox (proxy-blocked), confirmed again -- the agent's own web_fetch tool is the only viable path for live verification, and only for URLs that have appeared in a prior search result or fetch response (a "provenance" restriction that meant some direct API/URL guesses failed until reached via search results first).
License status: pagerduty-cronner is BSD-3-Clause (verified from the repo's own "License" sidebar and README section) -- permissive, on the approved list, metadata only, nothing copied. cartodb-labs-postgresql has no LICENSE file in the repo (verified from the file listing) -- recorded as license "none", cataloged as metadata only, nothing copied or adapted, so no THIRD_PARTY_NOTICES.md entry needed either way.
Decision: Only add candidates verified directly against their GitHub page (not just search-result snippets), and omit fields (like pushed_at) rather than guess when no reliable server-rendered date exists -- this is why darkcorners and DmitrysEngine (both promising, MIT-licensed, self-described-abandoned game engine/prototype candidates) were investigated but not added this run: their commit dates couldn't be verified without a JS-capable fetch. Left as a lead for a future run that has access to a JS-rendering tool (e.g. Claude in Chrome) or finds their dates via another server-rendered source (release tags, README-stated dates).
Copied code: no
Attribution needed: no
Next action: Next research-focused run should (a) try to verify tapio/darkcorners and mrDIMAS/DmitrysEngine's actual last-push dates via a JS-capable fetch or their Releases/README, since both are otherwise good, permissively-licensed, thematically on-point candidates (abandoned game engine/prototype); (b) diversify beyond ops-tooling/workshops into game/creative/dataset-shaped entries per SEED.md's breadth; (c) consider re-verifying the original 5 seed entries' suspiciously-identical "500 stars" values.
