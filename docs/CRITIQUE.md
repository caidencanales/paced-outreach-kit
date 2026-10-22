# Critique of the system this kit came from

This kit is a rebuild of a working, single-person LinkedIn networking setup: Claude Code driving a signed-in Chrome through the Claude in Chrome extension, a JSON contact log, and a few Python helpers. It worked. Real coffee chats got booked from it. A review of about 90 logged contacts over three weeks found these problems. Each one is now handled in code, not in a note to the model.

| # | What went wrong | Why it matters | What the kit does now |
|---|---|---|---|
| 1 | 44 connection requests went out on a single day, with nothing in the code to stop it. | Bursts are what get LinkedIn accounts restricted. | `pace.can_send` enforces daily and weekly caps, a minimum gap, a forced break after a streak, and business hours. `check` refuses early sends. |
| 2 | Seven people accepted and then waited up to two weeks for a first message. | An accepted request is the warmest moment you get, and it was wasted. | `due` lists accepted-but-unmessaged people first, with a default 2-day target. |
| 3 | The same message was drafted for six people at one company. | They talk to each other, and it reads as a blast. | Lint fails a draft that's 85% or more similar to anything already sent at that company. |
| 4 | Status was free text ("Invitation pending; sent without note…"), with 30+ different field names. Statuses went stale: accepted people still said "pending". | A tracker you can't trust gets ignored. | One SQLite file and an event log. Status is computed from events, never typed by hand. |
| 5 | LinkedIn and email lived in two separate trackers. | The same person could be contacted twice, or followed up on the wrong channel. | One `people` table. Every event records its channel. Duplicates are refused by URL, email, or name plus company. |
| 6 | The free-account note limit was hard-coded, but the account had already upgraded to Premium. | The system planned around a limit that no longer existed. | Limits and caps live in `config.json`, and the interview asks which account type you have. |
| 7 | Replies sat in the LinkedIn inbox without being logged. Nobody knew which message style worked. | Without a feedback loop, nothing improves. | Every send records its template. `report` shows accept, reply and meeting rates per template. The run routine checks the inbox first. |
| 8 | There was no do-not-contact list and no opt-out line. | It's disrespectful, and illegal in commercial email. | A `suppress` list, filled automatically on opt-out. Email templates get a footer with an address and an opt-out line, and lint fails without them. |
| 9 | Personalization was a habit, not a requirement. | Under time pressure, generic messages slip through. | Every template must use `{detail}`, and lint fails if the detail is too thin. |
| 10 | Pacing relied on the model remembering to wait. | Models don't wait reliably. | `next_action_at` is computed and `check` refuses to approve an early send. |
| 11 | It only ran from one Windows folder, and hard-coded paths broke in git worktrees. | Nobody else could use it. | Paths are handled by `pathlib`, `OUTREACH_HOME` relocates everything, and setup instructions cover each OS. |
| 12 | Scores were words ("HIGH", "MEDIUM-HIGH") with no evidence attached. | Not comparable, and not checkable. | Weighted 0-5 signals. Any signal above 0 needs an evidence URL. There's a configurable contact threshold. |
| 13 | Personal data sat next to code that could be pushed. | Leaks other people's information. | `config.json`, `data/` and `private/` are git-ignored, and `RULES.md` forbids publishing them. |
| 14 | No tests. | Every change was a guess. | Unit tests cover duplicates, derived status, opt-outs, pacing, breaks, lint and scoring. |

## Still not solved (be honest with the user)
- **LinkedIn's terms.** Any software-assisted messaging is against LinkedIn's User Agreement. Human approval and human volume lower the risk but don't remove it.
- **Email deliverability.** This kit doesn't warm up domains or check SPF, DKIM or DMARC. Send from a properly configured domain, start slowly, and watch bounces.
- **Reply detection is manual.** You, or Claude reading your inbox during a session, log replies. Nothing listens in the background.
- **Sourcing quality depends on judgment.** The rubric makes judgment explicit and checkable. It doesn't replace it.
