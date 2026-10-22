"""Templates with {placeholders}, rendered per person and linted before anyone sees them.

Template file format (templates/<name>.md):

    ---
    channel: linkedin        # linkedin | email
    kind: note               # note | message | email | followup
    subject: optional, email only, may use {placeholders}
    ---
    Hi {first_name}, {detail} ...

A template must use {detail}: one true, specific thing about this person. Lint fails without it.
"""
import difflib
import json
import re
from pathlib import Path

from .config import ROOT

EXAMPLE_SENDER = json.loads((ROOT / "config.example.json").read_text(encoding="utf-8"))["sender"]

PLACEHOLDER = re.compile(r"\{([a-z_]+)\}")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF]")


def load(cfg, name):
    path = Path(name) if Path(name).exists() else cfg["_templates"] / (name if name.endswith(".md") else name + ".md")
    raw = path.read_text(encoding="utf-8")
    meta, body = {}, raw
    if raw.startswith("---"):
        _, head, body = raw.split("---", 2)
        for line in head.strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.split("#")[0].strip()
    meta.setdefault("channel", "linkedin")
    meta.setdefault("kind", "message")
    meta["name"] = path.stem
    return meta, body.strip()


def variables(cfg, person, extra):
    s = cfg["sender"]
    v = {"sender_name": s["name"], "sender_role": s["role"], "organization": s["organization"],
         "program_name": s["program_name"], "program_one_liner": s.get("program_one_liner", ""), "apply_url": s["apply_url"], "postal_address": s["postal_address"]}
    if person is not None:
        v.update({k: person[k] for k in person.keys() if person[k] is not None})
    v.update(extra)
    return v


def render(cfg, meta, body, vars_):
    fill = lambda t: PLACEHOLDER.sub(lambda m: str(vars_.get(m.group(1), m.group(0))), t)
    main, subject = fill(body), fill(meta.get("subject", ""))
    text = main + ("\n\n" + fill(cfg["sender"]["email_footer"]) if meta["channel"] == "email" else "")
    return subject, main, text


def lint(cfg, meta, body, subject, main, text, vars_, prior_same_company=()):
    """Returns a list of (level, message). Any FAIL blocks the draft."""
    L, lim, out = cfg["lint"], cfg["limits"], []
    fail = lambda m: out.append(("FAIL", m))
    warn = lambda m: out.append(("WARN", m))
    unset = [k for k, v in EXAMPLE_SENDER.items()
             if k not in ("timezone", "email_footer") and v and v in subject + text]
    if unset:
        fail("config.json sender still has example values: " + ", ".join(unset))
    left = sorted(set(PLACEHOLDER.findall(subject + " " + text)))
    if left:
        fail("unfilled placeholders: " + ", ".join("{%s}" % x for x in left))
    if "{detail}" not in body:
        fail("template has no {detail}: every message needs one true thing specific to this person")
    elif len(str(vars_.get("detail", ""))) < L["min_detail_chars"]:
        fail(f"detail is too thin (<{L['min_detail_chars']} chars); use something only true of this person")
    low = (subject + " " + text).lower()
    for phrase in L["banned_phrases"]:
        if phrase in low:
            fail(f"banned phrase: {phrase!r}")
    if "—" in text or "–" in text:
        fail("em/en dash reads as machine-written; use a comma or period")
    if text.count("!") > L["max_exclamations"]:
        fail(f"more than {L['max_exclamations']} exclamation mark(s)")
    if not L["allow_emoji"] and EMOJI.search(text):
        fail("emoji not allowed by config")
    if meta["channel"] == "linkedin":
        cap = lim["linkedin_note"] if meta["kind"] == "note" else lim["linkedin_message"]
        if meta["kind"] == "note" and len(text) > lim["linkedin_note_hard"]:
            fail(f"note is {len(text)} chars; LinkedIn's limit is {lim['linkedin_note_hard']}")
        elif len(text) > cap:
            (fail if meta["kind"] != "note" else warn)(f"{len(text)} chars; aim for {cap} or fewer")
    else:
        if not subject:
            fail("email needs a subject")
        if len(subject) > lim["email_subject"]:
            warn(f"subject is {len(subject)} chars; under {lim['email_subject']} reads better on phones")
        words = len(main.split())
        if words > lim["email_body_words"]:
            fail(f"body is {words} words; cap is {lim['email_body_words']}")
        if "no thanks" not in low and "unsubscribe" not in low:
            fail("email has no opt-out line")
    for s in re.split(r"(?<=[.!?])\s+", text):
        if len(s.split()) > 32:
            warn(f"long sentence ({len(s.split())} words): {s[:50]}...")
    for prev in prior_same_company:
        r = difflib.SequenceMatcher(None, prev.lower(), main.lower()).ratio()
        if r >= L["duplicate_similarity"]:
            fail(f"{int(r * 100)}% the same as a message already sent to someone at this company")
    return out
