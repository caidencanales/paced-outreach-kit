---
description: One human-paced outreach session. Due items first, then new people, every send approved by the user
argument-hint: "[how many new people, default 3]"
---

Run one outreach session. New people this session: $ARGUMENTS (default 3). The rules in `docs/RULES.md` apply. Narrate each step in one short line; the user may be recording.

1. `python -m outreach pace`. If nothing's left, or we're outside business hours, say so and stop.
2. Check the LinkedIn notifications and inbox, and the email inbox if a connector is available, for accepts and replies. Log each verified one (`accepted`, `reply`, `optout`, `bounce`).
3. `python -m outreach due`. Handle these first: accepted-but-unmessaged people, then follow-ups.
4. Then the best new people: `python -m outreach list --status found --min-score <threshold>`.
5. For each person, one at a time:
   a. Re-read their profile or latest post and pick or refresh the `{detail}`.
   b. `python -m outreach draft <ref> <template> detail="..." [other=vars]`. On FAIL, fix the input, never the rule.
   c. `python -m outreach check <channel> <type>`. If it says WAIT, research the next person until `next_action_at`.
   d. LinkedIn: open the profile, click Connect or Message, type the text (no Enter key; it can send), stop before Send. Email: create a draft, or show the text for the user to paste.
   e. Ask "Send this to <name>?" with the exact text. Send only after a clear yes for this one, or let them click it.
   f. Verify it (Pending, the thread, or the Sent folder), then `python -m outreach log <ref> <channel> <type> "<text>" --template <name>`.
6. Stop immediately on any LinkedIn warning, limit notice, security check or CAPTCHA, or a run of email bounces.
7. Wrap up: what was sent, what's pending, budget left, and who's due next session. Add one line to `private/HANDOFF.md`.
