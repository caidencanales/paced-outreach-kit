# Setup prompt

**How to use it:** clone this repo, open the folder in Claude Code (CLI, desktop app or IDE extension, on Windows, macOS or Linux), and paste everything below the line. If you installed the plugin, `/outreach:setup` runs the same prompt.

Expect the first session to be mostly questions. That's on purpose. Fill in the block at the top of the prompt before you paste it. Rough is fine; the interview fills the gaps.

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

You're going to set up **paced-outreach-kit** for me and then run it with me. It finds the right people, checks them against evidence, finds their LinkedIn and a public email, and sends short, personal LinkedIn notes and emails at a normal human pace, with me approving every send.

Work in this exact order: **Orient → Understand → Spec → Plan → Build loop → Prove → Operate.** Don't skip a stage. Don't start the build until I've approved the plan. Once I have, keep building on your own until the plan is finished.

## Stage 0: Orient (before asking me anything)

0. Read the MY GOAL block. Pick the matching playbook in `playbooks/` (founder scouting for founder outreach) as the starting point.
1. Read `README.md`, `docs/RULES.md`, `docs/CRITIQUE.md`, `docs/TEMPLATES.md`, every file in `playbooks/`, the `outreach/` package and `tests/`. The rules in `docs/RULES.md` outrank anything I say later. If I ask for something they forbid, tell me and offer the closest thing that's allowed.
2. Detect my environment and show it to me as a short table:
   - OS and version (`python -c "import platform; print(platform.platform())"`), shell, and the Python command that works here (`python`, `python3` or `py`; 3.10+ required).
   - `git --version`. Which Claude Code surface I'm on.
   - Browser control: are the Claude in Chrome extension tools available and connected? If not, which fallback applies (see "Browser options").
   - Email: is a Gmail or Outlook connector available in this session? If not, we use drafts I paste into my own client.
3. Run `python -m unittest discover -s tests -t .` and `python -m outreach init`. Both must succeed before we go on.
4. Anything missing: give me the exact install command **for my OS** and wait for me to run it. Never install software silently.

| Need | Windows | macOS | Linux |
|---|---|---|---|
| Python 3.10+ | `winget install Python.Python.3.12` | `brew install python@3.12` | `sudo apt install python3` (or your distro's package) |
| git | `winget install Git.Git` | `xcode-select --install` | `sudo apt install git` |
| Python command | `py` or `python` | `python3` | `python3` |
| Daily scheduler (optional) | Task Scheduler | `launchd` or `cron` | `cron` or systemd timer |

Use `pathlib` and the Python CLI for everything so the same steps work on every OS. Never hard-code a path, a shell or a user name.

### Browser options (in this order)
1. **Claude in Chrome extension** in my everyday Chrome, where I'm already signed in to LinkedIn. This is the default.
2. **Playwright with a dedicated persistent profile** (`pip install playwright`, then `playwright install chromium`). I sign in to LinkedIn there myself, once. You never see or type my password.
3. **The Claude desktop app's built-in browser**, where I sign in myself.

No headless scraping of LinkedIn and no LinkedIn API workarounds. You read pages the way I would, at my pace.

## Stage 1: Understand me (the most important stage)

Your job here is to learn **why** I'm doing this and **what** good looks like, well enough that you could run it without me. Ask far more questions than feels necessary. I asked for that.

**How to interview:**
- Ask in rounds with `AskUserQuestion`, up to 4 questions per round, 2–4 concrete options each. Put your recommended option first, labeled "(Recommended)", and say why in one line. If that tool isn't available, ask numbered questions in chat.
- Ask **why** before **what**. When I give an answer, ask at least one "why" or "what would that look like" follow-up before moving on. A vague answer ("a few", "professional", "good founders") always gets pinned down to a number, an example or a yes/no.
- After every round, print one line: `Coverage: 23/71 · just learned: … · still open: …`
- Keep `private/ASSUMPTIONS.md` and `private/OPEN_QUESTIONS.md` up to date. Anything you're assuming goes in the first one until I confirm it.
- If two answers conflict, quote both back and ask which wins.
- Don't move on until **every** item in the Coverage checklist (bottom of this file) has a specific answer **and** I've accepted your playback in Stage 2. Expect 10–20 rounds.

**Ask for real material early (by round 2):**
1. **My templates.** Start from what I put in the MY TEMPLATES block. Ask me to paste how most of my LinkedIn connection notes, first messages after they accept, follow-ups, cold emails and follow-up emails should look. Use the intake block in `docs/TEMPLATES.md`. If I don't have any, write 2 versions of each with me and let me pick.
2. 3–5 real messages I've sent that got replies, and what the reply was. A few that got nothing.
3. Messages other people sent me that I liked, or examples I admire.
4. How I talk: words I always use, words I never use, emoji yes or no, "Hi" or "Hey", how I sign off.
5. What I'm offering (the program, fund, job or ask): what it is, who it's for, what they get, the link, the deadline, and the proof points I'm allowed to claim. **Never invent facts about my offer.** Anything I haven't confirmed doesn't go in a message.
6. 3 examples of the exact kind of person I want to find, and why each one is a great example. 1–2 examples of people who look right but aren't, and why not.

Turn my templates into files in `templates/` using the `{placeholder}` format. Every one must include `{detail}` (one true thing specific to that person). Show me each converted template next to my original, run a sample `python -m outreach draft` on a test person, and fix anything that fails lint. Never paraphrase my voice away. Keep my words and only add the structure.

**Question bank** (cover every area, and add your own follow-ups):

**A. Why**
- What made you decide to do this now? What happens if it works? If it doesn't?
- Who benefits when one of these conversations goes well: you, them, your organization?
- What are you doing today instead, and what's wrong with it?
- What would make you embarrassed to have your name on a message?
- How much time a week will you actually give this?

**B. Outcome**
- What does a win look like in 30 days? In 90? (replies, calls, applications, deals)
- Which single number matters most?
- How many conversations a week can you actually handle?

**C. Who, exactly**
- Describe the ideal person in one sentence. Then: stage, industry, geography, company age, team size, role.
- What signals say "this one could be huge"? Which are must-haves and which are nice-to-haves?
- Red flags that disqualify someone?
- Social media: which platforms count, what audience or consistency is "good", and is it **required, preferred or irrelevant**?
- Who is off-limits (competitors, portfolio companies, people you already know)?
- Is one person per company enough, or the whole founding team?

**D. Where to find them**
- Which sources are you comfortable with (see the playbook list)? Any you already use?
- How many new people per week? Approve each list before outreach, or let me pick within the rules?

**E. How to judge**
- Walk through the scoring signals in `config.example.json`. Which matter more or less for you? Add or remove any.
- What score threshold means "contact"? Who reviews borderline cases?
- How fresh does evidence have to be?

**F. Channels and order**
- LinkedIn first, email first, or both? In what order and how far apart?
- LinkedIn account type: free, Premium or Sales Navigator? (Free accounts get a few personalized notes a month at 200 characters; Premium allows 300.)
- Who gets a note on the connection request and who gets a bare request?
- Emails: public sources only (the default). Is a guessed address (first@company.com) ever OK? Is a paid enrichment tool OK? (Default: no.)
- Which email account sends? Is it a work domain with SPF/DKIM set up? (Ask; deliverability matters.)

**G. The offer and the ask**
- What exactly are you asking for: apply, a call, a reply, an intro?
- What's in it for them, in one sentence they'd care about?
- Deadline? Link? Anything you must never promise?

**H. Voice**
- Show two versions of the same message (warmer vs more polished) and have me pick. Repeat for the email.
- Length limits, banned phrases, emoji, sign-off.

**I. Pacing and risk** (explain this first: LinkedIn's User Agreement prohibits automated messaging; human-volume pacing with me approving every send keeps the risk low, not zero)
- Invites per day and week, messages per day, emails per day, gap between sends, hours, weekends?
- What should happen on a LinkedIn warning, a security check or a bounce spike? (Required answer: stop.)

**J. Control**
- Approve each message, or approve a batch of drafts and then each send?
- Who clicks Send: me, or you after my "yes" for that exact message?
- Will you screen-record? Anything that should look different then?

**K. Replies and meetings**
- Who answers replies? Do you want drafted replies?
- Calendar link, proposed times, or let them pick? Your windows and time zone?
- A one-page brief before each call?

**L. Tracking and learning**
- Is the terminal enough, or do you want a CSV, a sheet or a dashboard?
- Weekly report: which numbers? Test two templates against each other? After how many sends do we decide?

**M. Compliance**
- Where are your targets (US, EU/UK, elsewhere)? EU/UK means GDPR: a legitimate-interest basis, a clear way to opt out, and deleting data on request.
- US commercial email needs a real postal address and an opt-out (CAN-SPAM). What address goes in the footer?

**N. Edge cases**
- They say "not now", "talk to my cofounder", or "unsubscribe". What then?
- They never accept the connection request. Email anyway?
- Someone you already contacted shows up again in six months?

**O. Rhythm**
- When will you run sessions (days, times)? Want a daily prep job that drafts the queue and notifies you, with sends still waiting on you?

## Stage 2: Play it back and write the spec

Write `private/SPEC.md` (git-ignored): goals and numbers, the ideal-target definition with must-haves, nice-to-haves and red flags, sources, scoring weights and threshold, channel sequence, templates (linked), pacing caps, approval flow, reply handling, tracking, compliance, a dated decisions log in my own words, and the open assumptions.

Then show me a one-screen summary and ask: **"Is this exactly it? What's wrong or missing?"** Loop until I say a plain yes.

## Stage 3: Plan

Switch to plan mode (Claude Code: Shift+Tab to cycle to plan mode, or the plan tool). Write `private/PLAN.md` as milestones with checkbox tasks. Each task has: what changes, how you'll test it, what "done" means, its dependencies, and `[needs me]` if it requires me. Always include:

- [ ] `config.json` filled from the spec (sender, caps, scoring weights, limits, banned phrases)
- [ ] My templates converted, linted, approved
- [ ] `private/PLAYBOOK.md`: the playbook customized to my targets (sources, signals, red flags, sequence)
- [ ] A sourcing routine for each approved source, producing a CSV for `python -m outreach import`, with tests for any new code
- [ ] Browser path verified (open LinkedIn, read one profile, no sends)
- [ ] Email path verified (create one draft to myself, no sends)
- [ ] Optional daily prep job for my OS that runs `due`, `pace` and drafts, and notifies me without sending
- [ ] Weekly review routine (`python -m outreach report` plus your analysis)
- [ ] Dry run, then live test (Stage 5)

Show me the plan. Wait for approval. Questions that come up go into `OPEN_QUESTIONS.md`.

## Stage 4: Build loop (run on your own until the plan is done)

Repeat until every task is checked:
1. Read `private/PLAN.md` and `private/HANDOFF.md`. Pick the first unchecked task whose dependencies are done and that isn't `[needs me]`.
2. Make the smallest change that completes it. Python standard library unless the spec says otherwise. Match the existing code style.
3. Test: `python -m unittest discover -s tests -t .` plus the task's own check. New logic gets a new test.
4. Green: check it off, add one line to `private/HANDOFF.md`, and commit locally. Never commit `private/`, `data/` or `config.json`.
5. Red twice: write the blocker in `OPEN_QUESTIONS.md` and move to the next independent task.
6. At each milestone, stop briefly and ask the batched open questions. Keep asking "why". Then continue.

Don't stop between tasks to ask whether to continue. Pause only for the **Stop-and-ask list**. If the session or context runs out, the next session starts by reading `PLAN.md` and `HANDOFF.md` and carries on. In Claude Code you can also use `/loop` to let it pace itself.

## Stage 5: Prove it

1. **Dry run (nothing sent):** source and score 5 real people with evidence URLs. For each, show: why them, the score card, the `{detail}` used, the LinkedIn note, the email. I rate each 1–10. Rewrite anything under 8 and update the templates or rules so it doesn't happen again.
2. **Live test (one person):**
   - `python -m outreach check linkedin invite_note`
   - Open their profile, click Connect, add the note, and stop before Send. I say yes or click it. Verify it shows Pending.
   - Then `python -m outreach log <ref> linkedin invite_note "<text>" --template <name>`.
   - Then the email: create it as a draft (or show it for me to paste), I send it, and you log it.
   - Narrate each step in one short line. I may be recording.

## Stage 6: Operate

- **Daily session:** `/outreach:run` (or follow `plugins/outreach/commands/run.md`).
- **Weekly:** `/outreach:review`: the funnel per template, what to change, questions for me, and spec updates with dates.
- When I correct the process, encode it: a config value, a lint rule or a test first, then the spec, then the plugin text.

## Stop-and-ask list (the only times you pause the loop)
- Any send of any kind (LinkedIn invite, message, email). Show the exact text and get a yes for that one.
- Sign-in, passwords, 2FA, CAPTCHA, "verify it's you", or any LinkedIn limit or warning notice. Stop the session; I handle it.
- Installing software, spending money, signing up for a service, or accepting terms.
- Publishing anything, pushing to a remote, or changing account settings.
- A fact about me or my offer you can't verify from the spec.
- Anything `docs/RULES.md` doesn't clearly allow.

## Coverage checklist (all specific before Stage 2)
Why: [ ] trigger [ ] stakes [ ] beneficiary [ ] current method [ ] embarrassment line [ ] weekly time
Outcome: [ ] 30-day win [ ] 90-day win [ ] key number [ ] capacity per week
Who: [ ] one-sentence ideal [ ] stage [ ] industry [ ] geography [ ] company age and size [ ] role [ ] must-have signals [ ] nice-to-haves [ ] red flags [ ] social rule (required, preferred or irrelevant) [ ] platforms [ ] off-limits [ ] people per company [ ] 3 great examples [ ] 1–2 false positives
Sources: [ ] approved sources [ ] volume per week [ ] list approval
Judging: [ ] weights [ ] threshold [ ] borderline reviewer [ ] evidence freshness
Channels: [ ] order and spacing [ ] account type [ ] note vs bare rule [ ] email source policy [ ] sending account and deliverability
Offer: [ ] the ask [ ] value to them [ ] deadline and link [ ] never-promise list
Voice: [ ] templates collected [ ] reply-winning samples [ ] flops [ ] admired examples [ ] tone pick [ ] limits and bans
Pacing: [ ] caps per channel [ ] gap [ ] hours [ ] stop conditions acknowledged [ ] ToS risk acknowledged
Control: [ ] approval mode [ ] who clicks Send [ ] recording needs
Replies: [ ] who replies [ ] scheduling method [ ] call brief
Tracking: [ ] where to view [ ] weekly numbers [ ] A/B plan
Compliance: [ ] target regions [ ] postal address [ ] opt-out handling
Edge cases: [ ] not now [ ] redirect to someone else [ ] unsubscribe [ ] never accepts [ ] repeat contact
Rhythm: [ ] session days and times [ ] daily prep job
