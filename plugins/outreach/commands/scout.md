---
description: Find and score new people from approved public sources, slowly, with evidence for every point
argument-hint: "<who to look for, e.g. 'AI infra founders who launched on Show HN this month'> [how many, default 10]"
---

Scout for: **$ARGUMENTS**

Follow `private/PLAYBOOK.md` if it exists, otherwise the matching file in `playbooks/`. The rules in `docs/RULES.md` apply. Narrate one short line per step.

1. `python -m outreach brief`. If profile views for today are used up, stop.
2. **Candidates.** Use the sources approved in `private/SPEC.md`. The built-in ones are `python -m outreach source hn --days 14 --min-points 50` and `python -m outreach source github --days 60 --min-stars 300 [--query "topic:ai"]`. Each writes a CSV in `private/candidates/`. Read any other source in the browser.
3. **Research each candidate, one at a time, slowly.** Before opening any page, run `python -m outreach check browse view`. On WAIT, finish reading what's open or write notes. After opening a page, run `python -m outreach viewed <url>`. Read the product, the founder's About page and their recent posts properly. Don't skim twenty tabs.
   - `python -m outreach find <name or company>`: skip anyone already logged or suppressed.
   - Identify the founder by real name (company site or team page), confirm their LinkedIn (the current title matches), and find a public email in the playbook order, recording `email_source`.
   - Score with `python -m outreach score <ref> '<card>'`. Every point needs a URL you read. Note social presence (preferred, not required, unless the spec says otherwise).
   - Write one `{detail}`: the single most specific true thing you found, with its URL, in `notes`.
4. Show a table: name, company, score, social yes/no, the detail, LinkedIn URL, email source. Ask which to keep. Add the kept ones (`add`, or `import` a CSV). Nothing is sent during scouting.
