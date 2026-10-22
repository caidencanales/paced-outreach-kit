---
description: Set up paced-outreach-kit (or resume setup). Get the kit, deep interview, spec, plan, then an autonomous build loop, dry run and live test
argument-hint: "[what you want outreach for, optional]"
---

What I want outreach for (if given): $ARGUMENTS

1. **Find the kit.** If the current folder has no `outreach/cli.py`, look for a `paced-outreach-kit` folder here or one level down. If there isn't one, clone https://github.com/caidencanales/paced-outreach-kit.git and work inside it. Tell me to reopen Claude Code in that folder when convenient, so the session brief loads.
2. **Resume, don't restart.** If `private/PLAN.md` exists, read `private/HANDOFF.md` and `private/PLAN.md`, run `python -m outreach brief`, tell me in one line where we are, and continue the build loop from the first unchecked task. If `private/SPEC.md` exists without a plan, continue at Stage 3.
3. **Otherwise** read `SETUP_PROMPT.md` in the kit and follow it exactly, starting at Stage 0. The plugin is already installed, since you're running this command.

Slow is the point: `check` before every send, and `check browse view` and `viewed` around every page you open.
