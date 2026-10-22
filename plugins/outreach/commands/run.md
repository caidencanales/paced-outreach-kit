---
description: One slow, human-paced outreach session. Due items first, then new people, every send approved
argument-hint: "[how many new people, default 3]"
---

Run one outreach session. New people this session: $ARGUMENTS (default 3). The rules in `docs/RULES.md` apply. Narrate each step in one short line; the user may be recording. **Go slowly.** The pacing commands decide when, not you.

1. `python -m outreach brief`. If no budget is left, or we're outside business hours, say so and stop.
2. **Inbox first.** Check LinkedIn notifications and messages, and the email inbox if a connector is available, for accepts, replies, opt-outs and bounces. Log each verified one. A reply goes to the user. Draft an answer only if asked.
3. **Due list.** `python -m outreach due`: accepted-but-unmessaged people first, then follow-ups. Then the best new people from `python -m outreach list --status found --min-score <threshold from config>`.
4. **Draft.** For each person: re-read their profile or latest post (`check browse view`, then `viewed <url>`), pick or refresh the `{detail}`, and run `python -m outreach draft <ref> <template> detail="..."` (`--eml` for email without a connector). On FAIL, fix the input, never the rule.
5. **Approve** (from `approval` in `config.json`):
   - `each`: show one exact draft, then "Send this to <name>?"
   - `batch`: show every draft numbered with its exact text. The user answers with the numbers they approve ("send 1, 2, 4"). Any edit means that draft needs a new yes.
6. **Send, one at a time.** For each approved draft:
   a. `python -m outreach check <channel> <type>`. On WAIT, prepare the next person (read their profile, refine the detail) until `next_action_at`. Never send early.
   b. LinkedIn: open the profile, click Connect or Message, type the exact approved text (no Enter key; it can send), and click Send, or let the user click it. Email: send the approved draft through the connector, or the user sends the `.eml` from their mail app.
   c. Verify it (Pending, the thread, or the Sent folder). Then `python -m outreach log <ref> <channel> <type> "<text>" --template <name>`.
   d. Every 5 sends, the pacing forces a break. Use it to scout or tidy notes.
7. Stop immediately on any LinkedIn warning, limit notice, security check or CAPTCHA, or a run of bounces.
8. Wrap up: what was sent, what's pending, budget left, and who's due next session. Add one line to `private/HANDOFF.md`.
