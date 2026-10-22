---
description: Weekly review. What's working per template and source, what to change, and questions for the user
---

1. `python -m outreach report` and `python -m outreach due`. Also `export` to a temporary CSV if you need to slice by source or score.
2. Compare accept, reply and meeting rates by template, by source, by score band, and with or without social presence. Call out anything with fewer than 10 sends as too early to judge.
3. Check pacing history: any day near a cap? Any warnings? Any opt-outs or bounces, and what they had in common?
4. Propose at most 3 changes (a template edit, a scoring weight, a source to drop or add, a cap). Each one cites the numbers.
5. Ask the user at least 5 questions about what they're seeing that the numbers don't show: reply quality, who they enjoyed talking to, what felt off.
6. Apply only the changes they approve. Encode them in config, templates or tests, then log them with a date in `private/SPEC.md`.
