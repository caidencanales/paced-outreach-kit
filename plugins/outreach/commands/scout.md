---
description: Find and score new people for outreach from approved public sources, with evidence for every point
argument-hint: "<who to look for, e.g. 'AI infra founders who launched on Show HN this month'> [how many, default 10]"
---

Scout for: **$ARGUMENTS**

Follow `private/PLAYBOOK.md` if it exists, otherwise the matching file in `playbooks/`. The rules in `docs/RULES.md` apply.

1. Use only the sources approved in `private/SPEC.md`. Read pages in the user's browser (Claude in Chrome first). Narrate in one short line per step.
2. For each candidate, run `python -m outreach find <name or company>` first. Skip anyone already logged or suppressed.
3. Confirm identity: company site name matches LinkedIn, and the current title matches. If it's ambiguous, skip and say why.
4. Find a public email following the playbook order. Record `email_source`. Never guess unless the spec allows it.
5. Score with `python -m outreach score <ref> '<card>'`. Every point needs a URL you read this session. Note `has_social`.
6. Write down one `{detail}` per person: the single most specific true thing you found, with its URL, in `notes`.
7. Show a table: name, company, score, social yes/no, the detail, LinkedIn URL, email source. Ask which to keep. Add the kept ones with `add` (or `import` for many) and send nothing.
