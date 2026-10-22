# Templates

Templates live in `templates/<name>.md`. A small header says which channel and kind they are, and the body uses `{placeholders}`:

```
---
channel: linkedin        # linkedin | email
kind: note               # note | message | followup | email
subject: {company} and {program_name}   # email only
---
Hi {first_name}! {detail} I help founders through {program_name} and would love to connect.
```

Render and lint one for a person with:

```
python -m outreach draft <ref> linkedin_note detail="Your Show HN post on the offline-first editor was great."
```

## Placeholders
- **The person** (any field in the log): `{first_name}`, `{name}`, `{company}`, `{title}`, `{linkedin_url}`, `{email}`
- **You** (from `config.json` → `sender`): `{sender_name}`, `{sender_role}`, `{organization}`, `{program_name}`, `{program_one_liner}`, `{apply_url}`, `{postal_address}`
- **Per message** (passed as `key=value`): `{detail}` (required in every template), plus anything you invent, like `{deadline}` or `{mutual}`

## What lint enforces (settings in `config.json` → `lint` and `limits`)
- Every placeholder is filled in. Sender fields aren't still the example values.
- `{detail}` is used, and it's specific enough (at least 15 characters by default).
- No banned phrases, em dashes, extra exclamation marks, or emoji (unless allowed).
- LinkedIn notes fit LinkedIn's limit. Messages and email bodies stay under their caps.
- Emails have a subject and the footer with your address and an opt-out line.
- The message isn't nearly the same as one already sent to someone at the same company.

## Template intake (paste this to Claude during setup)

Fill in what you have. Blank is fine; Claude will write two versions with you.

```
CONNECTION NOTE (how most of mine should look):

FIRST MESSAGE AFTER THEY ACCEPT:

LINKEDIN FOLLOW-UP:

COLD EMAIL (subject + body):

FOLLOW-UP EMAIL:

RULES I ALWAYS FOLLOW (length, greeting, sign-off, emoji, etc.):

THINGS I NEVER SAY:

MESSAGES THAT GOT REPLIES (paste + what they said):

MESSAGES THAT GOT NOTHING:

EXAMPLES FROM OTHER PEOPLE I LIKE:
```

Claude converts these into template files, keeps your wording, adds the placeholders, shows you each one next to your original, and lints a sample before you approve it.
