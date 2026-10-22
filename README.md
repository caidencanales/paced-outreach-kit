# paced-outreach-kit

Personal, evidence-backed outreach on LinkedIn and email, run by Claude Code at a human pace, with **you approving every send**.

It finds the right people, scores them against evidence, finds their LinkedIn and a public email, drafts short messages from **your own templates**, refuses anything generic, duplicated, too fast or untrue, and tracks what actually gets replies.

It ships with two playbooks:
- **Founder scouting:** find exceptional early founders (ideally ones who also build in public) and invite them to apply to your fund, fellowship, accelerator or community.
- **Networking and coffee chats:** recruiters, alumni and people a few years ahead of you.

Any other outreach works too. The setup interview adapts it.

## How it works

```
 you + Claude Code ──► SETUP_PROMPT.md: orient → deep interview → spec → plan → build loop → dry run → live test
                         │
 sources (public) ──► python -m outreach import / add ──► score (0-5 per signal, evidence URL required)
                         │
 your templates ────► draft + lint ({detail} required, no banned phrases, no near-duplicates, length caps)
                         │
 Claude in Chrome ──► opens LinkedIn, types the note, stops at Send ──► you say yes ──► log (verified)
 email connector  ──► creates a draft ──► you send ──► log
                         │
                     pace / check (caps, variable gaps, breaks, hours, research pace)   due   report (what works)
```

## Quick start (Windows, macOS or Linux)

You need Python 3.10+, git, [Claude Code](https://claude.com/claude-code), and ideally the Claude in Chrome extension.

```bash
git clone https://github.com/caidencanales/paced-outreach-kit.git
cd paced-outreach-kit
python -m unittest discover -s tests -t .
python -m outreach init
```

On macOS and Linux, use `python3` if `python` isn't found. On Windows, `py` works too.

Easiest: open Claude Code in an empty folder and paste [SETUP_PROMPT.md](SETUP_PROMPT.md). It clones this repo, installs the plugin and starts the interview.

**The plugin is required.** It provides `/outreach:setup`, `/outreach:scout`, `/outreach:run` and `/outreach:review`, plus a brief at the start of every session in the kit folder:

```bash
claude plugin marketplace add caidencanales/paced-outreach-kit
claude plugin install outreach@paced-outreach-kit
```

(Or type `/plugin marketplace add caidencanales/paced-outreach-kit` and `/plugin install outreach@paced-outreach-kit` inside Claude Code.) Then restart Claude Code in the `paced-outreach-kit` folder and run `/outreach:setup`.

## Commands

| Command | What it does |
|---|---|
| `python -m outreach init` | creates `config.json` and `data/` (both git-ignored) |
| `brief` | one screen: budget left, what's due, pipeline, next step (also shown at session start) |
| `source hn` / `source github` | free public founder discovery: Show HN launches and fast-growing new repos, written to a candidates CSV |
| `viewed <url>` / `check browse view` | research pace: a gap between profile views and a daily view cap |
| `add '<json>'` / `import file.csv` | adds people; refuses duplicates and do-not-contact entries |
| `find <words>` / `show <ref>` / `list` | checks the log |
| `score <ref> '<card>'` | weighted score; evidence URL required for every point |
| `draft <ref> <template> detail="..." [--eml]` | renders and lints a message; exits 1 on any FAIL; `--eml` saves an email draft any mail app opens |
| `pace` / `check <channel> <type>` | what's left today; whether you may send right now |
| `log <ref> <channel> <type> "text" --template t` | records an event after you verified it happened |
| `due` | accepted-but-unmessaged people and follow-ups due today |
| `report` | accept, reply and meeting rate per template; busiest day |
| `suppress <email|domain|url>` | never contact again |
| `export file.csv` | everything as a spreadsheet |

Plugin commands: `/outreach:setup`, `/outreach:scout`, `/outreach:run`, `/outreach:review`.

## Rules

Read [docs/RULES.md](docs/RULES.md). In short: you approve every send; you handle sign-ins and CAPTCHAs; everything said is true and sourced; opt-outs are permanent; and it goes **slowly**. Sends and research are both rate-limited with variable gaps, so a session works like a careful person, not a script.

[docs/CRITIQUE.md](docs/CRITIQUE.md) covers what went wrong in the system this was rebuilt from and how each problem is now handled in code.

## Privacy

Your `config.json`, `data/` (the contact database) and `private/` (your spec, plan and notes) are git-ignored, so they stay on your machine.

## License

MIT
