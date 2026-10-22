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
                     pace / check (daily + weekly caps, gaps, breaks, hours)   due (follow-ups)   report (what works)
```

## Quick start (Windows, macOS or Linux)

You need Python 3.10+, git, [Claude Code](https://claude.com/claude-code), and ideally the Claude in Chrome extension.

```bash
git clone https://github.com/<you>/paced-outreach-kit.git
cd paced-outreach-kit
python -m unittest discover -s tests -t .
python -m outreach init
```

On macOS and Linux, use `python3` if `python` isn't found. On Windows, `py` works too.

Then open the folder in Claude Code and paste the contents of [SETUP_PROMPT.md](SETUP_PROMPT.md). Or install the plugin and run `/outreach:setup`:

```
/plugin marketplace add ./
/plugin install outreach@paced-outreach-kit
```

## Commands

| Command | What it does |
|---|---|
| `python -m outreach init` | creates `config.json` and `data/` (both git-ignored) |
| `add '<json>'` / `import file.csv` | adds people; refuses duplicates and do-not-contact entries |
| `find <words>` / `show <ref>` / `list` | checks the log |
| `score <ref> '<card>'` | weighted score; evidence URL required for every point |
| `draft <ref> <template> detail="..."` | renders and lints a message; exits 1 on any FAIL |
| `pace` / `check <channel> <type>` | what's left today; whether you may send right now |
| `log <ref> <channel> <type> "text" --template t` | records an event after you verified it happened |
| `due` | accepted-but-unmessaged people and follow-ups due today |
| `report` | accept, reply and meeting rate per template; busiest day |
| `suppress <email|domain|url>` | never contact again |
| `export file.csv` | everything as a spreadsheet |

Plugin commands: `/outreach:setup`, `/outreach:scout`, `/outreach:run`, `/outreach:review`.

## Rules

Read [docs/RULES.md](docs/RULES.md). In short: a human sends or approves every message; the human handles sign-ins and CAPTCHAs; everything said is true and sourced; public emails only; opt-outs are permanent; human volume only. **LinkedIn's User Agreement prohibits automated messaging.** This kit keeps a human in the loop and the volume low, which reduces the risk but doesn't remove it.

[docs/CRITIQUE.md](docs/CRITIQUE.md) covers what went wrong in the system this was rebuilt from and how each problem is now handled in code.

## Privacy

Your `config.json`, `data/` (the contact database) and `private/` (your spec, plan and notes) never leave your machine and are git-ignored. If you fork this publicly, keep it that way.

## License

MIT
