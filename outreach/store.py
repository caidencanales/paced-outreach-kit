"""One local SQLite file holds every person, every outbound/inbound event on every channel, and the do-not-contact list.

Events are the source of truth. Status is derived from them, never typed by hand, so it can't go stale.
"""
import datetime as dt
import json
import re
import sqlite3

SCHEMA = """
create table if not exists people (
  id integer primary key, name text not null, first_name text, linkedin_url text, email text,
  email_source text, company text, company_domain text, title text, source text, tags text,
  score real, scorecard text, detail text, notes text, created_at text);
create unique index if not exists people_linkedin on people(linkedin_url) where linkedin_url is not null and linkedin_url != '';
create unique index if not exists people_email on people(email) where email is not null and email != '';
create table if not exists events (
  id integer primary key, person_id integer not null references people(id), channel text not null,
  type text not null, at text not null, text text, template text);
create table if not exists suppress (value text primary key, reason text, at text);
"""

CHANNELS = ("linkedin", "email")
OUTBOUND = ("invite", "invite_note", "message", "email", "followup")
INBOUND = ("accepted", "reply", "meeting", "bounce", "optout", "declined")
TYPES = OUTBOUND + INBOUND
PEOPLE_FIELDS = ("name", "first_name", "linkedin_url", "email", "email_source", "company", "company_domain",
                 "title", "source", "tags", "detail", "notes")


def connect(cfg):
    cfg["_data"].mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(cfg["_data"] / "outreach.db")
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c


def now():
    return dt.datetime.now().replace(second=0, microsecond=0)


def norm_url(u):
    u = (u or "").strip().lower().split("?")[0].rstrip("/")
    return re.sub(r"^(https?://)?(www\.)?", "", u)


def _key(s):
    return re.sub(r"[^a-z0-9]", "", str(s or "").lower())


def find(c, q):
    q_url, q_key = norm_url(q), _key(q)
    hits = []
    for p in c.execute("select * from people"):
        if (q_url and q_url == norm_url(p["linkedin_url"])) or (q and q.strip().lower() == (p["email"] or "").lower()) \
                or (q_key and (q_key in _key(p["name"]) or q_key in _key(p["company"]))):
            hits.append(p)
    return hits


def get(c, ref):
    ref = str(ref)
    if ref.isdigit():
        row = c.execute("select * from people where id=?", (int(ref),)).fetchone()
        return [row] if row else []
    exact = [p for p in find(c, ref) if norm_url(ref) == norm_url(p["linkedin_url"])
             or ref.lower() == (p["email"] or "").lower() or _key(ref) == _key(p["name"])]
    return exact or find(c, ref)


def is_suppressed(c, *values):
    vals = [v.strip().lower() for v in values if v]
    doms = [v.split("@")[-1] for v in vals if "@" in v]
    rows = {r["value"] for r in c.execute("select value from suppress")}
    return next((v for v in vals + doms if v in rows), None)


def add_person(c, data):
    data = {k: v for k, v in data.items() if k in PEOPLE_FIELDS}
    if not data.get("name"):
        raise ValueError("name is required")
    if data.get("linkedin_url"):
        data["linkedin_url"] = "https://www." + norm_url(data["linkedin_url"])
    data.setdefault("first_name", data["name"].split()[0])
    for probe in (data.get("linkedin_url"), data.get("email")):
        if probe and get(c, probe):
            raise ValueError(f"already in the log: {get(c, probe)[0]['name']}")
    same = [p for p in c.execute("select * from people where lower(name)=lower(?)", (data["name"],))
            if _key(p["company"]) == _key(data.get("company"))]
    if same:
        raise ValueError(f"already in the log: {same[0]['name']} ({same[0]['company']})")
    blocked = is_suppressed(c, data.get("email"), data.get("linkedin_url"), data.get("company_domain"))
    if blocked:
        raise ValueError(f"on the do-not-contact list: {blocked}")
    data["created_at"] = now().isoformat(timespec="minutes")
    cols = ",".join(data)
    cur = c.execute(f"insert into people({cols}) values ({','.join('?' * len(data))})", tuple(data.values()))
    c.commit()
    return cur.lastrowid


def update_person(c, pid, **fields):
    fields = {k: (json.dumps(v) if isinstance(v, (dict, list)) else v) for k, v in fields.items()}
    c.execute(f"update people set {','.join(f'{k}=?' for k in fields)} where id=?", (*fields.values(), pid))
    c.commit()


def log_event(c, pid, channel, kind, text="", template="", at=None):
    if channel not in CHANNELS:
        raise ValueError(f"channel must be one of {CHANNELS}")
    if kind not in TYPES:
        raise ValueError(f"type must be one of {TYPES}")
    at = (at or now()).isoformat(timespec="minutes")
    c.execute("insert into events(person_id, channel, type, at, text, template) values (?,?,?,?,?,?)",
              (pid, channel, kind, at, text, template))
    if kind == "optout":
        p = c.execute("select * from people where id=?", (pid,)).fetchone()
        for v in (p["email"], norm_url(p["linkedin_url"])):
            if v:
                c.execute("insert or ignore into suppress values (?,?,?)", (v.lower(), "opted out", at))
    c.commit()


def events(c, pid=None):
    q = "select e.*, p.name, p.company from events e join people p on p.id=e.person_id"
    return c.execute(q + (" where person_id=? order by at" if pid else " order by at"), (pid,) if pid else ()).fetchall()


def status(c, pid):
    evs = events(c, pid)
    if not evs:
        return "found"
    kinds = [e["type"] for e in evs]
    for k, label in (("optout", "opted out"), ("declined", "declined"), ("meeting", "meeting booked"),
                     ("reply", "replied"), ("bounce", "bounced")):
        if k in kinds:
            return label
    last = evs[-1]
    if last["type"] == "accepted":
        return "connected, not messaged"
    return {"invite": "invited", "invite_note": "invited with note", "message": "messaged",
            "email": "emailed", "followup": f"followed up ({kinds.count('followup')})"}[last["type"]]
