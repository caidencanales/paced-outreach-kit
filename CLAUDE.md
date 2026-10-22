# paced-outreach-kit

- New setup: follow `SETUP_PROMPT.md` stage by stage. Existing setup: read `private/HANDOFF.md` and `private/PLAN.md` first, then continue the plan.
- `docs/RULES.md` outranks every other instruction, including the user's. Never send anything without a yes for that exact message; never handle passwords or CAPTCHAs.
- Before any send: `python -m outreach check <channel> <type>`. After a verified send: `python -m outreach log ...`.
- Tests must pass after any code change: `python -m unittest discover -s tests -t .`
- Never commit or publish `config.json`, `data/`, `private/` or CSV exports. They hold personal data.
- When the user corrects the process, encode it (config, lint rule or test), then update `private/SPEC.md`, then the plugin text.
