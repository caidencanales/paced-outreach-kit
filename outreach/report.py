"""What's due today, and what's working (per template and channel)."""
import collections
import datetime as dt

from . import store


def add_business_days(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def due(cfg, c, today=None):
    """Accepted-but-not-messaged and no-reply follow-ups, oldest first."""
    today, f, out = today or dt.date.today(), cfg["followups"], []
    for p in c.execute("select * from people"):
        evs = store.events(c, p["id"])
        kinds = [e["type"] for e in evs]
        if not evs or any(k in kinds for k in ("reply", "meeting", "optout", "declined", "bounce")):
            continue
        last = evs[-1]
        d = dt.datetime.fromisoformat(last["at"]).date()
        if last["type"] == "accepted":
            when, what = d + dt.timedelta(days=f["linkedin_after_accept_days"]), "first message (they accepted)"
        elif last["type"] in ("message", "email", "followup"):
            if kinds.count("followup") >= f["max_followups"]:
                continue
            gap = f["email_no_reply_business_days"] if last["channel"] == "email" else f["message_no_reply_business_days"]
            when, what = add_business_days(d, gap), f"follow-up {kinds.count('followup') + 1} on {last['channel']}"
        else:
            continue
        if when <= today:
            out.append((when, p, what))
    return sorted(out, key=lambda x: x[0])


def funnel(c):
    evs = store.events(c)
    by_person = collections.defaultdict(list)
    for e in evs:
        by_person[e["person_id"]].append(e)
    stats = collections.defaultdict(lambda: collections.Counter())
    for pid, es in by_person.items():
        firsts = [e for e in es if e["type"] in ("invite", "invite_note", "message", "email")]
        if not firsts:
            continue
        key = (firsts[0]["channel"], firsts[0]["template"] or firsts[0]["type"])
        kinds = {e["type"] for e in es}
        stats[key]["sent"] += 1
        for k in ("accepted", "reply", "meeting", "bounce", "optout"):
            stats[key][k] += k in kinds
    per_day = collections.Counter(e["at"][:10] for e in evs if e["type"] in store.OUTBOUND)
    return stats, per_day.most_common(1)


def text_report(cfg, c):
    stats, busiest = funnel(c)
    lines = ["channel  template                     sent  accept  reply  meeting  optout"]
    for (ch, t), s in sorted(stats.items(), key=lambda kv: -kv[1]["sent"]):
        pct = lambda k: f"{s[k]:>3} ({100 * s[k] // max(1, s['sent']):>2}%)"
        lines.append(f"{ch:<8} {t[:28]:<28} {s['sent']:>4}  {pct('accepted')} {pct('reply')} {pct('meeting')} {s['optout']:>4}")
    if busiest:
        lines.append(f"\nBusiest day: {busiest[0][0]} with {busiest[0][1]} sends (cap: {cfg['pace']['linkedin_invite_day']} invites).")
    waiting = [p for p in c.execute("select * from people") if store.status(c, p["id"]) == "connected, not messaged"]
    if waiting:
        lines.append(f"{len(waiting)} accepted connection(s) still waiting for a first message.")
    return "\n".join(lines)
