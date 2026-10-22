---
name: outreach-rules
description: Standing rules for paced-outreach-kit. Use whenever the user talks about LinkedIn outreach, connection requests, cold emails to founders or anyone, coffee chats, scouting people, or follow-ups in this kit.
---

# Outreach rules (short form of docs/RULES.md)

- **Commands:** `/outreach:setup` (first time, or to resume), `/outreach:scout`, `/outreach:run`, `/outreach:review`. Kit: https://github.com/caidencanales/paced-outreach-kit
- **Slow is the point.** Run `python -m outreach check <channel> <type>` before every send. While researching, run `check browse view` before and `viewed <url>` after every page you open. WAIT means do careful work in between (read properly, refine the next draft), never work around it. Gaps vary on purpose, and breaks are forced after streaks.
- **Sending:** type the message or create the draft, then stop. Send only after a yes for that exact text (or that numbered draft in `batch` mode), or the user clicks it.
- **Accounts:** sign-ins, passwords, 2FA, CAPTCHAs and any limit or warning notice mean stop and hand over to the user.
- **Truth:** facts about the user and the offer come only from `private/SPEC.md`. Facts about the recipient come from a page read this session. Score points need evidence URLs.
- **Personal:** every message uses one specific `{detail}`. Lint must PASS. No near-identical messages within a company.
- **Respect no:** opt-outs and bounces are logged (`optout`, `bounce`) and never contacted again.
- **Logging:** only after verifying it happened.
- **Data stays local:** `config.json`, `data/` and `private/` are git-ignored.
