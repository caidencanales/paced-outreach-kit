"""python -m outreach <command>   (run with no command for help)

  init                                   create data/ and config.json (git-ignored)
  brief                                  one-screen status: budget, what's due, pipeline counts, next steps
  source hn|github [--days N] [--min-points N|--min-stars N] [--query Q] [--out file.csv]
                                         find candidates from free public sources (see outreach/sources.py)
  add '<json>'                           new person; refuses duplicates and do-not-contact entries
  import <file.csv>                      bulk add (columns = person fields); duplicates are skipped with a reason
  find <words|url|email>                 already in the log?
  show <ref>                             one person, their scorecard and every event
  list [--status S] [--min-score N]      everyone, best score first
  score <ref> '<json card>'              evidence-backed score (see outreach/score.py)
  pace                                   what's left today and when the next send is allowed
  draft <ref> <template> [key=value...] [--eml]
                                         render + lint a message; exit 1 if anything FAILs;
                                         --eml also saves an email draft any mail app opens (private/drafts/)
  check <channel> <type>                 may I send this right now? (check browse view = may I open the next page?)
  viewed <url>                           record that you opened a profile or page (research pace)
  log <ref> <linkedin|email> <type> ["text"] [--template NAME]
                                         record an event AFTER verifying it really happened
  suppress <email|domain|url> [reason]   never contact again
  due                                    first messages and follow-ups due today
  report                                 funnel per template/channel, busiest day, waiting queue
  export <file.csv>                      everything as CSV

<ref> is an id, a LinkedIn URL, an email, or a unique name.
"""
import csv
import json
import shutil
import sys

import datetime as dt
from email.message import EmailMessage
from pathlib import Path

from . import config, pace, report, score, sources, store, templates


def one(c, ref):
    hits = store.get(c, ref)
    if len(hits) != 1:
        sys.exit(f"{len(hits)} people match {ref!r}. Use the id, URL or email." if hits else f"No one matches {ref!r}.")
    return hits[0]


def opt(args, flag, default=None):
    if flag in args:
        i = args.index(flag)
        val = args[i + 1]
        del args[i:i + 2]
        return val
    return default


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    cmd, args = args[0], args[1:]
    cfg = config.load()
    if cmd == "init":
        if not (cfg["_root"] / "config.json").exists():
            shutil.copy(config.ROOT / "config.example.json", cfg["_root"] / "config.json")
            print("Created config.json. Fill in the sender block before drafting anything.")
        store.connect(cfg)
        print(f"Database ready at {cfg['_data'] / 'outreach.db'}")
        return 0
    if cmd == "source":
        which = args[0] if args else ""
        out = opt(args, "--out", f"private/candidates/{which}-{dt.date.today()}.csv")
        days = int(opt(args, "--days", 14 if which == "hn" else 60))
        if which == "hn":
            rows = sources.hn(days, int(opt(args, "--min-points", 50)))
        elif which == "github":
            rows = sources.github(days, int(opt(args, "--min-stars", 300)), opt(args, "--query", ""))
        else:
            sys.exit("source must be hn or github")
        path = sources.write(rows, cfg["_root"] / out)
        print(f"{len(rows)} candidates -> {path}")
        for r in rows[:15]:
            print(f"  {r['signal']:<28} {r['handle'][:18]:<18} {r['project'][:60]}")
        return 0
    c = store.connect(cfg)

    if cmd == "brief":
        b = pace.budget(cfg, c)
        counts = {}
        for p in c.execute("select id from people"):
            s_ = store.status(c, p["id"])
            counts[s_] = counts.get(s_, 0) + 1
        rows = report.due(cfg, c)
        ready = c.execute("select count(*) from people where score >= ?",
                          (cfg["scoring"]["min_score_to_contact"],)).fetchone()[0]
        print(f"Budget: {b['linkedin_invites_today']} invites, {b['linkedin_messages_today']} LinkedIn messages, "
              f"{b['emails_today']} emails left today. Next send at {b['next_action_at']}"
              + ("" if b["in_business_hours"] else " (outside business hours)"))
        print("Pipeline: " + (", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "empty"))
        print(f"Due now: {len(rows)}")
        for _, p, what in rows[:10]:
            print(f"  #{p['id']} {p['name']}: {what}")
        found = counts.get("found", 0)
        nxt = ("handle what's due with /outreach:run" if rows else
               "send to the best scored people with /outreach:run" if found and ready else
               "find and score new people with /outreach:scout")
        print("Next: " + nxt)
    elif cmd == "add":
        try:
            pid = store.add_person(c, json.loads(args[0]))
        except ValueError as e:
            sys.exit(f"Not added: {e}")
        print(f"Added #{pid}.")
    elif cmd == "import":
        added, skipped = 0, []
        with open(args[0], newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                try:
                    store.add_person(c, {k.strip(): v.strip() for k, v in row.items() if k and v and v.strip()})
                    added += 1
                except ValueError as e:
                    skipped.append(f"{row.get('name', '?')}: {e}")
        print(f"Added {added}. Skipped {len(skipped)}.")
        for s_ in skipped:
            print("  skip", s_)
    elif cmd == "find":
        hits = store.find(c, " ".join(args))
        for p in hits:
            print(f"#{p['id']} {p['name']} | {p['title'] or ''} @ {p['company'] or ''} | {store.status(c, p['id'])}")
        print(f"{len(hits)} match(es)." if hits else "Not in the log.")
    elif cmd == "show":
        p = one(c, args[0])
        print(json.dumps({k: p[k] for k in p.keys()}, indent=2, ensure_ascii=False))
        print("status:", store.status(c, p["id"]))
        for e in store.events(c, p["id"]):
            print(f"  {e['at']} {e['channel']:<8} {e['type']:<11} {e['template'] or ''} {(e['text'] or '')[:80]}")
    elif cmd == "list":
        st, mn = opt(args, "--status"), float(opt(args, "--min-score", -1))
        for p in c.execute("select * from people order by coalesce(score, -1) desc, id"):
            s = store.status(c, p["id"])
            if (st and st not in s) or (p["score"] or 0) < mn:
                continue
            print(f"#{p['id']:<4} {p['score'] if p['score'] is not None else '-':>5}  {p['name'][:24]:<24} "
                  f"{(p['company'] or '')[:22]:<22} {s}")
    elif cmd == "score":
        p, card = one(c, args[0]), json.loads(args[1])
        r = score.score(cfg, card)
        for e in r["errors"]:
            print("FAIL", e)
        if r["missing"]:
            print("not scored yet:", ", ".join(r["missing"]))
        print(f"score {r['score']} | social presence: {'yes' if r['has_social'] else 'no'} | "
              f"{'contact' if r['contact'] else 'hold'} (threshold {cfg['scoring']['min_score_to_contact']})")
        if not r["errors"]:
            store.update_person(c, p["id"], score=r["score"], scorecard=card)
        return 1 if r["errors"] else 0
    elif cmd == "pace":
        for k, v in pace.budget(cfg, c).items():
            print(f"{k}: {v}")
    elif cmd == "viewed":
        store.log_view(c, args[0])
        b = pace.budget(cfg, c)
        print(f"Logged. {b['profile_views_today']} views left today; next page after {b['next_view_at']}.")
    elif cmd == "check":
        ok, why = pace.can_send(cfg, c, args[0], args[1], dt.datetime.now() if args[1] == "view" else None)
        print(("OK: " if ok else "WAIT: ") + why)
        return 0 if ok else 1
    elif cmd == "draft":
        eml = "--eml" in args
        args = [a for a in args if a != "--eml"]
        p = one(c, args[0])
        extra = dict(a.split("=", 1) for a in args[2:])
        if store.is_suppressed(c, p["email"], store.norm_url(p["linkedin_url"]), p["company_domain"]):
            sys.exit("This person is on the do-not-contact list.")
        meta, body = templates.load(cfg, args[1])
        vars_ = templates.variables(cfg, p, extra)
        subject, main, text = templates.render(cfg, meta, body, vars_)
        prior = [e["text"] for e in store.events(c) if e["company"] and e["company"] == p["company"]
                 and e["person_id"] != p["id"] and e["text"] and e["type"] in store.OUTBOUND]
        issues = templates.lint(cfg, meta, body, subject, main, text, vars_, prior)
        print(f"[{meta['channel']} {meta['kind']} to {p['name']}, template {meta['name']}]")
        if subject:
            print("Subject:", subject)
        print(text)
        print(f"\n({len(text)} chars, {len(main.split())} words)")
        for level, msg in issues:
            print(level, msg)
        if any(level == "FAIL" for level, _ in issues):
            return 1
        print("PASS")
        if eml:
            if not p["email"]:
                sys.exit("No email on file for this person.")
            m = EmailMessage()
            m["To"], m["Subject"], m["X-Unsent"] = p["email"], subject, "1"
            m.set_content(text)
            d = cfg["_root"] / "private" / "drafts"
            d.mkdir(parents=True, exist_ok=True)
            path = d / f"{p['id']}-{meta['name']}.eml"
            path.write_bytes(bytes(m))
            print(f"Draft saved: {path} (double-click to open it in your mail app, review, send)")
    elif cmd == "log":
        tmpl = opt(args, "--template", "")
        p = one(c, args[0])
        channel, kind, text = args[1], args[2], args[3] if len(args) > 3 else ""
        if kind in store.OUTBOUND:
            ok, why = pace.can_send(cfg, c, channel, kind)
            if not ok:
                print(f"Note: logged past the pacing rule ({why}). Slow down for the next one.")
        try:
            store.log_event(c, p["id"], channel, kind, text, tmpl)
        except ValueError as e:
            sys.exit(str(e))
        print(f"{p['name']}: {kind} on {channel} logged. Status: {store.status(c, p['id'])}")
    elif cmd == "suppress":
        c.execute("insert or replace into suppress values (?,?,?)",
                  (store.norm_url(args[0]) if "linkedin.com" in args[0] else args[0].lower(),
                   " ".join(args[1:]) or "do not contact", store.now().isoformat(timespec="minutes")))
        c.commit()
        print(f"{args[0]} will never be contacted.")
    elif cmd == "due":
        rows = report.due(cfg, c)
        for when, p, what in rows:
            print(f"#{p['id']} {p['name']} ({p['company'] or ''}): {what}, due {when}")
        print(f"{len(rows)} due." if rows else "Nothing due today.")
    elif cmd == "report":
        print(report.text_report(cfg, c))
    elif cmd == "export":
        rows = c.execute("select * from people").fetchall()
        with open(args[0], "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(list(rows[0].keys()) + ["status"] if rows else ["empty"])
            for r in rows:
                w.writerow(list(r) + [store.status(c, r["id"])])
        print(f"Wrote {len(rows)} people to {args[0]}")
    else:
        print(__doc__)
        return 2
    return 0
