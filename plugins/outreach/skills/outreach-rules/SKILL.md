---
name: outreach-rules
description: Standing rules for paced-outreach-kit. Use whenever the user talks about LinkedIn outreach, connection requests, cold emails to founders or anyone, coffee chats, scouting people, or follow-ups in this repo.
---

# Outreach rules (short form of docs/RULES.md)

- **Commands:** `/outreach:setup` (first time, or to resume the build), `/outreach:scout`, `/outreach:run`, `/outreach:review`.
- **Sending:** you may type a message into LinkedIn or create an email draft, then stop before Send. Send only after a clear yes for that exact text, or the user clicks it. One yes covers one send.
- **Accounts:** sign-ins, passwords, 2FA, CAPTCHAs and LinkedIn warnings mean you stop and hand over to the user.
- **Pace:** `python -m outreach check <channel> <type>` before every send. WAIT means research the next person, not send. No evasion tooling of any kind.
- **Truth:** facts about the user and the offer come from `private/SPEC.md` only. Facts about the recipient come from a page you read this session. Score points need evidence URLs.
- **Personal:** every message uses one specific `{detail}`. Lint must PASS. Never send near-identical messages within a company.
- **Email:** public addresses only, unless the spec allows otherwise. The footer with a real postal address and an opt-out line stays in. An opt-out or bounce means `log ... optout` or `bounce`, and they're never contacted again.
- **Logging:** only after verifying it happened. Never log a send that didn't happen.
- **Privacy:** never commit or publish `config.json`, `data/`, `private/` or exports.
