"""Human-paced sending budget. These caps keep volume at what one busy person does by hand.

Two speeds are limited: sends (invites, messages, emails) and research (opening profiles and pages). Gaps between sends
vary by a few minutes so the day doesn't run on a metronome. The person approves every send; this module refuses bursts.
"""
import datetime as dt

from . import store


def _bucket(channel, kind):
    if channel == "email":
        return "email"
    return "invite" if kind in ("invite", "invite_note") else "message"


def budget(cfg, c, at=None):
    p, at = cfg["pace"], at or store.now()
    today, week_ago = at.date(), at.date() - dt.timedelta(days=6)
    out = [e for e in store.events(c) if e["type"] in store.OUTBOUND]
    day = lambda e: dt.datetime.fromisoformat(e["at"]).date()
    count = lambda pred: sum(1 for e in out if pred(e))
    inv = lambda e: e["channel"] == "linkedin" and e["type"] in ("invite", "invite_note")
    left = {
        "linkedin_invites_today": min(p["linkedin_invite_day"] - count(lambda e: inv(e) and day(e) == today),
                                      p["linkedin_invite_week"] - count(lambda e: inv(e) and day(e) >= week_ago)),
        "linkedin_notes_month": p["linkedin_note_month"] - count(
            lambda e: e["type"] == "invite_note" and (day(e).year, day(e).month) == (today.year, today.month)),
        "linkedin_messages_today": p["linkedin_message_day"] - count(
            lambda e: e["channel"] == "linkedin" and e["type"] in ("message", "followup") and day(e) == today),
        "emails_today": p["email_day"] - count(lambda e: e["channel"] == "email" and day(e) == today),
    }
    left = {k: max(0, v) for k, v in left.items()}
    stamps = sorted(dt.datetime.fromisoformat(e["at"]) for e in out)
    nxt = at
    if stamps:
        jitter = int(stamps[-1].timestamp() // 60) % (p.get("jitter_minutes", 0) + 1)
        nxt = max(nxt, stamps[-1] + dt.timedelta(minutes=p["min_gap_minutes"] + jitter))
        streak = 1
        for a, b in zip(reversed(stamps[:-1]), reversed(stamps[1:])):
            if (b - a) >= dt.timedelta(minutes=p["break_minutes"]):
                break
            streak += 1
        if streak >= p["break_every"]:
            nxt = max(nxt, stamps[-1] + dt.timedelta(minutes=p["break_minutes"]))
    start, end = p["business_hours"]
    in_hours = start <= at.hour < end and (at.weekday() < 5 or not p["weekdays_only"])
    seen = [v for v in store.views(c) if v.date() == today]
    next_view = seen[-1] + dt.timedelta(seconds=p.get("view_gap_seconds", 0)) if seen else at
    return {**left, "profile_views_today": max(0, p.get("profile_views_day", 10 ** 6) - len(seen)),
            "next_action_at": nxt.strftime("%Y-%m-%d %H:%M"), "next_view_at": max(next_view, at).strftime("%H:%M:%S"),
            "in_business_hours": in_hours}


def can_send(cfg, c, channel, kind, at=None):
    at = at or store.now()
    b = budget(cfg, c, at)
    if kind == "view":
        if b["profile_views_today"] <= 0:
            return False, "profile views for today are used up; stop researching and come back tomorrow"
        nv = dt.datetime.combine(at.date(), dt.time.fromisoformat(b["next_view_at"]))
        if at < nv:
            return False, f"slow down; open the next page after {b['next_view_at']} (read this one properly first)"
        return True, "ok"
    key = {"invite": "linkedin_invites_today", "message": "linkedin_messages_today", "email": "emails_today"}[
        _bucket(channel, kind)]
    if b[key] <= 0:
        return False, f"{key} is used up"
    if kind == "invite_note" and b["linkedin_notes_month"] <= 0:
        return False, "personalized notes for this month are used up; send without a note"
    if at < dt.datetime.fromisoformat(b["next_action_at"]):
        return False, f"too soon; next send allowed at {b['next_action_at']} (use the time to research the next person)"
    if not b["in_business_hours"]:
        return False, "outside business hours in config.pace"
    return True, "ok"
