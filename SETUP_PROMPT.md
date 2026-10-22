# Setup prompt

**Repo:** https://github.com/caidencanales/paced-outreach-kit

**How to use it:** open Claude Code (CLI, desktop app or IDE extension, on Windows, macOS or Linux) in any empty folder. Fill in the block at the top of the prompt below (rough is fine), then paste the whole thing. Claude downloads the kit, installs the plugin, and walks you through everything. Expect the first session to be mostly questions. That's on purpose.

---

```
MY GOAL (1-2 lines):
  e.g. Find exceptional early-stage startup founders who could build the next big company (bonus if they
  build in public on social media, not required), find each founder's LinkedIn and a public email,
  and invite them to apply to +EV.

MY TEMPLATES (paste how most of my LinkedIn notes, messages and emails should look, or write "help me write them"):
  CONNECTION NOTE:
  FIRST MESSAGE AFTER THEY ACCEPT:
  COLD EMAIL (subject + body):
  FOLLOW-UP:
```

You're going to set up **paced-outreach-kit** (https://github.com/caidencanales/paced-outreach-kit) for me and then run it with me. It finds the right people, checks them against evidence, finds their LinkedIn and a public email, and sends short, personal LinkedIn notes and emails at a slow, human pace, with me approving every send.

Work in this exact order: **Get the kit → Orient → Understand → Spec → Plan → Build loop → Prove → Operate.** Don't skip a stage. Don't start the build until I've approved the plan. Once I have, keep building on your own until the plan is finished.

**Slow is the point.** Never rush outreach. Before every send, run `python -m outreach check <channel> <type>`. Before opening each profile or page while researching, run `python -m outreach check browse view`, and after opening it, `python -m outreach viewed <url>`. When either says WAIT, read what's in front of you more carefully or prepare the next draft. Never try to get around a WAIT. A slow day that books one great conversation beats a fast day that burns twenty names.

## Get the kit and the plugin (required; the commands and the session brief come from the plugin)

1. If this folder doesn't already contain `outreach/cli.py`, clone the kit and work inside it from now on:
   `git clone https://github.com/caidencanales/paced-outreach-kit.git` then `cd paced-outreach-kit`.
   If git is missing, give me the install command for my OS (table below) and wait.
2. Install the plugin (user scope):
   ```
   claude plugin marketplace add caidencanales/paced-outreach-kit
   claude plugin install outreach@paced-outreach-kit
   claude plugin list
   ```
   If the CLI isn't available here, tell me to type these in Claude Code instead:
   `/plugin marketplace add caidencanales/paced-outreach-kit`, then `/plugin install outreach@paced-outreach-kit`.
3. Confirm `outreach@paced-outreach-kit` is listed and enabled. Tell me to restart Claude Code **in the `paced-outreach-kit` folder** and type `/outreach:setup`. It picks up exactly where this leaves off, and from then on every session there starts with the day's brief.
4. Updates later: `claude plugin marketplace update paced-outreach-kit`, then `git pull` in the kit folder.

## Stage 0: Orient (before asking me anything)

0. Read the MY GOAL block. Pick the matching playbook in `playbooks/` (`founder-scouting.md` for founder outreach) as the starting point.
1. Read `README.md`, `docs/RULES.md`, `docs/CRITIQUE.md`, `docs/TEMPLATES.md`, the playbooks, the `outreach/` package and `tests/`. The rules in `docs/RULES.md` outrank everything else.
2. Detect my environment and show it to me as a short table: OS and version, shell, the Python command that works (`python`, `python3` or `py`; 3.10+ required), git, which Claude Code surface I'm on, whether the plugin is installed, whether the Claude in Chrome extension is connected, and whether a Gmail or Outlook connector is available (if not, emails go out as `.eml` drafts from `draft --eml`).
3. Run `python -m unittest discover -s tests -t .`, `python -m outreach init` and `python -m outreach brief`. All three must succeed.
4. Anything missing: give me the exact command **for my OS** and wait. Never install anything silently.

| Need | Windows | macOS | Linux |
|---|---|---|---|
| Python 3.10+ | `winget install Python.Python.3.12` | `brew install python@3.12` | `sudo apt install python3` |
| git | `winget install Git.Git` | `xcode-select --install` | `sudo apt install git` |
| Python command | `py` or `python` | `python3` | `python3` |
| Daily prep job (optional) | Task Scheduler | `launchd` or `cron` | `cron` |

Use `pathlib` and the Python CLI so every step works on every OS. Never hard-code a path, a shell or a user name.

**Browser, in this order:** (1) the Claude in Chrome extension in my everyday signed-in Chrome; (2) Playwright with a dedicated persistent profile I sign in to once (`pip install playwright` then `playwright install chromium`); (3) the Claude desktop app's built-in browser, signed in by me.

## Stage 1: Understand me (the most important stage)

Your job is to learn **why** I'm doing this and **what** good looks like, well enough that you could run it without me. Ask far more questions than feels necessary. I asked for that.

**How to interview:**
- Ask in rounds with `AskUserQuestion`, up to 4 questions per round, 2–4 concrete options each. Put your recommended option first with "(Recommended)" and give the reason in one line. If that tool isn't available, ask numbered questions in chat.
- Ask **why** before **what**. Every answer gets at least one follow-up ("why does that matter?", "show me an example", "what number?"). A vague answer always gets pinned down.
- After every round, print one line: `Coverage: 23/70 · just learned: … · still open: …`
- Keep `private/ASSUMPTIONS.md` and `private/OPEN_QUESTIONS.md` current. Everything you're assuming goes in the first file until I confirm it.
- If two answers conflict, quote both and ask which wins.
- Don't move on until every item in the Coverage checklist is specific **and** I've accepted the playback in Stage 2. Expect 10–20 rounds.

**Get real material early (by round 2):**
1. **My templates.** Start from the MY TEMPLATES block, then use the intake block in `docs/TEMPLATES.md` for the rest: connection notes, first messages after they accept, LinkedIn follow-ups, cold emails, follow-up emails. If I don't have any, write two versions of each with me and let me pick.
2. 3–5 real messages I've sent that got replies, and what the reply said. A few that got nothing.
3. Messages from other people that I liked.
4. How I talk: words I always use, words I never use, emoji yes or no, "Hi" or "Hey", sign-off.
5. My offer (for example +EV): what it is, who it's for, what they get, the link, the deadline, and the proof points I'm allowed to claim. **Never invent facts about the offer.**
6. 3 examples of exactly the kind of person I want, and why each one is great. 1–2 who look right but aren't, and why not.

Turn my templates into files in `templates/` with `{placeholders}`, each one using `{detail}`. Show each next to my original, run `python -m outreach draft` on a test person, and fix lint failures. Keep my words; only add structure.

**Question bank** (cover every area, add your own follow-ups):

**A. Why:** What made you start this now? What happens if it works, and if it doesn't? Who benefits when a conversation goes well? What are you doing today instead, and what's wrong with it? What would embarrass you to have your name on? How many hours a week will you really give this?

**B. Outcome:** What's a win at 30 days, and at 90 (replies, calls, applications)? Which single number matters most? How many conversations a week can you handle?

**C. Who exactly:** The ideal person in one sentence. Then stage, industry, geography, company age, team size, role. Which signals say "this could be huge", and which are must-haves versus nice-to-haves? Red flags? Social media: which platforms, what counts as "good", and is it **required, preferred or irrelevant**? Who's off-limits? One founder per company, or the whole team?

**D. Where to find them:** Which sources (the playbook list, plus the built-in `source hn` and `source github`)? Any you already use? How many new people a week? Do you approve each list, or do I pick within the rules?

**E. How to judge:** Go through the scoring signals in `config.json` and adjust the weights, adding or removing signals. What score means "contact"? Who decides borderline cases? How fresh must evidence be?

**F. Channels and order:** LinkedIn first, email first, or both, in what order and how far apart? Free, Premium or Sales Navigator (note limits and length)? Who gets a note and who gets a bare connection request? Emails: public only, or are guessed patterns or an enrichment tool OK? Which account sends, and is the domain set up for deliverability (SPF/DKIM)?

**G. The offer and the ask:** Exactly what are you asking for (apply, a call, a reply, an intro)? What's in it for them, in one sentence they'd care about? Deadline and link? Anything you must never promise?

**H. Voice:** Show two versions of the same message (warmer vs more polished) and have me pick. Do the same for the email. Length limits, banned phrases, emoji, sign-off.

**I. Pace:** Invites per day and per week, messages per day, emails per day, the gap between sends, profile views per day, hours, weekends? (The defaults in `config.example.json` are deliberately slow. Only loosen them if I insist, and say what you'd watch for.) What should happen on a LinkedIn warning, a security check or a bounce spike? (Stop.)

**J. Control:** Approval mode `each` (one by one) or `batch` (I approve a numbered list of exact drafts, then you send them one at a time at the paced rate)? Who clicks Send? Will I screen-record?

**K. Replies and meetings:** Who answers replies? Do you want drafted replies? Calendar link, proposed times, or let them pick? My windows and time zone? A one-page brief before each call?

**L. Tracking and learning:** Is the terminal enough, or do I want a CSV, a sheet or a dashboard? Which numbers go in the weekly review? Test two templates against each other, and after how many sends do we decide?

**M. Email basics:** What postal address goes in the email footer? Is the opt-out wording OK?

**N. Edge cases:** "Not now"? "Talk to my cofounder"? "Unsubscribe"? Never accepts the connection request (email anyway)? Someone we contacted resurfaces months later?

**O. Rhythm:** Which days and times are sessions? Do I want a daily prep job that drafts the queue and notifies me, with sends still waiting on me?

## Stage 2: Play it back and write the spec

Write `private/SPEC.md` (git-ignored): goals and numbers, the ideal target (must-haves, nice-to-haves, red flags), sources, scoring weights and threshold, channel sequence, templates, pace caps, approval mode, reply handling, tracking, a dated decisions log in my own words, and the open assumptions. Put the numbers into `config.json`.

Show a one-screen summary and ask: **"Is this exactly it? What's wrong or missing?"** Loop until I say a plain yes.

## Stage 3: Plan

Switch to plan mode (Shift+Tab in Claude Code, or the plan tool). Write `private/PLAN.md` as milestones with checkbox tasks. Each task has: what changes, how it's tested, what "done" means, its dependencies, and `[needs me]` if it requires me. Always include:

- [ ] `config.json` matches the spec (sender, approval mode, pace, scoring, limits, banned phrases)
- [ ] My templates converted, linted and approved
- [ ] `private/PLAYBOOK.md`: the playbook tailored to my targets
- [ ] A sourcing routine for every approved source, built on `source hn` / `source github` / the browser, ending in `import`, with tests for new code
- [ ] Browser path verified (open one profile, `viewed`, no sends)
- [ ] Email path verified (one draft to myself, no sends)
- [ ] Optional daily prep job for my OS (`brief`, `due`, drafts, a notification, no sends)
- [ ] Weekly review routine (`/outreach:review`)
- [ ] Dry run, then live test (Stage 5)

Show me the plan and wait for approval.

## Stage 4: Build loop (run on your own until the plan is done)

Repeat until every task is checked:
1. Read `private/PLAN.md` and `private/HANDOFF.md`. Pick the first unchecked task whose dependencies are done and that isn't `[needs me]`.
2. Make the smallest change that completes it, carefully. Python standard library unless the spec says otherwise. Match the existing style.
3. Test: `python -m unittest discover -s tests -t .` plus the task's own check. New logic gets a new test.
4. Green: check it off, add one line to `private/HANDOFF.md`, commit locally. Never commit `private/`, `data/` or `config.json`.
5. Red twice: write the blocker in `OPEN_QUESTIONS.md` and move to the next independent task.
6. At each milestone, stop and ask the batched open questions. Keep asking why. Then continue.

Don't stop between tasks to ask whether to continue. Pause only for the Stop-and-ask list. If the session ends, the next session (`/outreach:setup`) reads `PLAN.md` and `HANDOFF.md` and carries on. `/loop` can pace it in Claude Code.

## Stage 5: Prove it

1. **Dry run (nothing sent):** source and score 5 real people with evidence URLs, at the research pace. For each, show why them, the score card, the `{detail}`, the LinkedIn note and the email. I rate each 1–10. Rewrite anything under 8, and change the template or rule so it doesn't happen again.
2. **Live test (one person):** `check` → open the profile (`check browse view`, then `viewed`) → Connect → add the note → stop before Send → I say yes or click it → verify it shows Pending → `log ... --template <name>`. Then the email: a draft (connector, or `draft --eml`) → I send it → you log it. Narrate each step in one short line; I may be recording.

## Stage 6: Operate

- **Daily:** `/outreach:run` (it starts from `brief`: due items first, then new people).
- **Scouting:** `/outreach:scout <who>`.
- **Weekly:** `/outreach:review`: the funnel per template, source and score band, at most 3 changes backed by numbers, and questions for me.
- When I correct the process, encode it in config, a lint rule or a test first, then the spec, then the plugin text.

## Stop-and-ask list (the only times the loop pauses)
- Any send (LinkedIn invite, message, email) not covered by my yes for that exact text.
- Sign-in, passwords, 2FA, CAPTCHA, "verify it's you", or any LinkedIn limit or warning notice. Stop the session; I handle it.
- Installing software, spending money, signing up for a service, or accepting terms.
- Pushing to a remote, publishing anything, or changing account settings.
- A fact about me or my offer that isn't in the spec.

## Coverage checklist (all specific before Stage 2)
Why: [ ] trigger [ ] stakes [ ] beneficiary [ ] current method [ ] embarrassment line [ ] weekly time
Outcome: [ ] 30-day win [ ] 90-day win [ ] key number [ ] capacity per week
Who: [ ] one-sentence ideal [ ] stage [ ] industry [ ] geography [ ] company age and size [ ] role [ ] must-have signals [ ] nice-to-haves [ ] red flags [ ] social rule [ ] platforms [ ] off-limits [ ] people per company [ ] 3 great examples [ ] 1–2 false positives
Sources: [ ] approved sources [ ] volume per week [ ] list approval
Judging: [ ] weights [ ] threshold [ ] borderline reviewer [ ] evidence freshness
Channels: [ ] order and spacing [ ] account type [ ] note vs bare rule [ ] email source policy [ ] sending account and deliverability
Offer: [ ] the ask [ ] value to them [ ] deadline and link [ ] never-promise list
Voice: [ ] templates collected [ ] reply-winning samples [ ] flops [ ] admired examples [ ] tone pick [ ] limits and bans
Pace: [ ] send caps [ ] gap [ ] research pace [ ] hours [ ] stop conditions
Control: [ ] approval mode [ ] who clicks Send [ ] recording needs
Replies: [ ] who replies [ ] scheduling method [ ] call brief
Tracking: [ ] where to view [ ] weekly numbers [ ] A/B plan
Email basics: [ ] postal address [ ] opt-out wording
Edge cases: [ ] not now [ ] redirect to someone else [ ] unsubscribe [ ] never accepts [ ] repeat contact
Rhythm: [ ] session days and times [ ] daily prep job
