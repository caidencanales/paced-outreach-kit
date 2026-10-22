import datetime as dt
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import contextlib
import io

from outreach import cli, config, pace, report, score, sources, store, templates

ROOT = Path(__file__).resolve().parent.parent


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        shutil.copytree(ROOT / "templates", self.tmp / "templates")
        os.environ["OUTREACH_HOME"] = str(self.tmp)
        (self.tmp / "config.json").write_text(json.dumps({"sender": {
            "name": "Sam Sender", "role": "partner", "organization": "Test Fund", "program_name": "Test Program",
            "program_one_liner": "We give early founders a small check and a peer group.",
            "apply_url": "https://test.example/apply", "postal_address": "PO Box 1, Testville"}}))
        self.cfg = config.load()
        self.c = store.connect(self.cfg)
        self.pid = store.add_person(self.c, {"name": "Ada Example", "linkedin_url": "https://linkedin.com/in/ada-example/",
                                             "email": "ada@example.com", "company": "ExampleCo",
                                             "company_domain": "example.com"})

    def tearDown(self):
        self.c.close()
        os.environ.pop("OUTREACH_HOME", None)
        shutil.rmtree(self.tmp, ignore_errors=True)


class StoreTests(Base):
    def test_duplicates_refused_by_url_email_and_name(self):
        for dup in ({"name": "X", "linkedin_url": "www.linkedin.com/in/ada-example"},
                    {"name": "Y", "email": "ADA@example.com"},
                    {"name": "Ada Example", "company": "ExampleCo"}):
            with self.assertRaises(ValueError):
                store.add_person(self.c, dup)

    def test_status_is_derived_from_events(self):
        self.assertEqual(store.status(self.c, self.pid), "found")
        store.log_event(self.c, self.pid, "linkedin", "invite")
        store.log_event(self.c, self.pid, "linkedin", "accepted")
        self.assertEqual(store.status(self.c, self.pid), "connected, not messaged")
        store.log_event(self.c, self.pid, "linkedin", "reply")
        self.assertEqual(store.status(self.c, self.pid), "replied")

    def test_optout_suppresses_person_and_blocks_readd(self):
        store.log_event(self.c, self.pid, "email", "optout")
        self.assertTrue(store.is_suppressed(self.c, "ada@example.com"))
        store.add_person(self.c, {"name": "Other"})
        self.c.execute("insert into suppress values ('blocked.com', 'test', 'now')")
        with self.assertRaises(ValueError):
            store.add_person(self.c, {"name": "Z", "email": "z@blocked.com"})


class PaceTests(Base):
    def test_gap_daily_cap_and_break(self):
        t = dt.datetime(2030, 1, 7, 10, 0)  # a Monday
        self.assertTrue(pace.can_send(self.cfg, self.c, "linkedin", "invite", t)[0])
        store.log_event(self.c, self.pid, "linkedin", "invite", at=t)
        self.assertFalse(pace.can_send(self.cfg, self.c, "linkedin", "invite", t + dt.timedelta(minutes=1))[0])
        p = self.cfg["pace"]
        earliest = dt.datetime.fromisoformat(pace.budget(self.cfg, self.c, t)["next_action_at"])
        self.assertTrue(t + dt.timedelta(minutes=p["min_gap_minutes"]) <= earliest
                        <= t + dt.timedelta(minutes=p["min_gap_minutes"] + p["jitter_minutes"]))
        self.assertTrue(pace.can_send(self.cfg, self.c, "linkedin", "invite", earliest)[0])
        for i in range(1, 5):
            store.log_event(self.c, self.pid, "linkedin", "invite", at=t + dt.timedelta(minutes=4 * i))
        ok, why = pace.can_send(self.cfg, self.c, "linkedin", "invite", t + dt.timedelta(minutes=20))
        self.assertFalse(ok, "5 sends in a row should force a break")
        self.assertTrue(pace.can_send(self.cfg, self.c, "linkedin", "invite", t + dt.timedelta(minutes=40))[0])

    def test_research_pace(self):
        t = dt.datetime(2030, 1, 7, 10, 0, 0)
        self.assertTrue(pace.can_send(self.cfg, self.c, "browse", "view", t)[0])
        store.log_view(self.c, "https://linkedin.com/in/someone", t)
        self.assertFalse(pace.can_send(self.cfg, self.c, "browse", "view", t + dt.timedelta(seconds=10))[0])
        self.assertTrue(pace.can_send(self.cfg, self.c, "browse", "view", t + dt.timedelta(seconds=46))[0])

    def test_weekend_and_daily_cap(self):
        sat = dt.datetime(2030, 1, 12, 10, 0)
        self.assertFalse(pace.can_send(self.cfg, self.c, "email", "email", sat)[0])
        mon = dt.datetime(2030, 1, 7, 9, 0)
        for i in range(self.cfg["pace"]["linkedin_invite_day"]):
            store.log_event(self.c, self.pid, "linkedin", "invite", at=mon + dt.timedelta(minutes=30 * i))
        later = mon + dt.timedelta(hours=7, minutes=50)
        self.assertEqual(pace.budget(self.cfg, self.c, later)["linkedin_invites_today"], 0)


class TemplateTests(Base):
    def draft(self, name, **extra):
        meta, body = templates.load(self.cfg, name)
        p = self.c.execute("select * from people where id=?", (self.pid,)).fetchone()
        v = templates.variables(self.cfg, p, extra)
        subject, main, text = templates.render(self.cfg, meta, body, v)
        return templates.lint(self.cfg, meta, body, subject, main, text, v), text

    def test_good_note_passes(self):
        issues, text = self.draft("linkedin_note", detail="Your launch post on the offline-first editor was great.")
        self.assertFalse([m for lvl, m in issues if lvl == "FAIL"], issues)

    def test_missing_detail_and_banned_phrase_fail(self):
        issues, _ = self.draft("linkedin_note", detail="hi")
        self.assertTrue(any("too thin" in m for _, m in issues))
        issues, _ = self.draft("linkedin_note", detail="I hope this finds you well, loved your work.")
        self.assertTrue(any("banned phrase" in m for _, m in issues))

    def test_email_needs_every_placeholder_and_footer(self):
        issues, text = self.draft("email_followup", detail="Saw the new pricing page went live this week.")
        self.assertTrue(any("{deadline}" in m for _, m in issues))
        issues, text = self.draft("email_first", detail="Saw the new pricing page went live this week.")
        self.assertIn("no thanks", text.lower())

    def test_near_duplicate_at_same_company_fails(self):
        meta, body = templates.load(self.cfg, "linkedin_note")
        v = {"first_name": "Bo", "detail": "Your launch post on the offline-first editor was great.",
             "program_name": "Prog"}
        subject, main, text = templates.render(self.cfg, meta, body, v)
        issues = templates.lint(self.cfg, meta, body, subject, main, text, v, prior_same_company=[main])
        self.assertTrue(any("the same as a message" in m for _, m in issues))


class ScoreAndReportTests(Base):
    def test_example_sender_values_fail(self):
        os.remove(self.tmp / "config.json")
        cfg = config.load()
        meta, body = templates.load(cfg, "linkedin_note")
        v = templates.variables(cfg, None, {"first_name": "Bo", "detail": "Your launch post on the editor was great."})
        subject, main, text = templates.render(cfg, meta, body, v)
        self.assertTrue(any("example values" in m for _, m in templates.lint(cfg, meta, body, subject, main, text, v)))

    def test_score_requires_evidence(self):
        r = score.score(self.cfg, {"traction": {"value": 4}})
        self.assertTrue(r["errors"])
        r = score.score(self.cfg, {"traction": {"value": 5, "evidence": "https://example.com/post"},
                                   "social_audience": {"value": 3, "evidence": "https://example.com/x"}})
        self.assertFalse(r["errors"])
        self.assertTrue(r["has_social"])
        self.assertGreater(r["score"], 0)

    def test_due_after_accept_and_followups_stop(self):
        old = dt.datetime.now() - dt.timedelta(days=10)
        store.log_event(self.c, self.pid, "linkedin", "accepted", at=old)
        self.assertEqual(len(report.due(self.cfg, self.c)), 1)
        store.log_event(self.c, self.pid, "linkedin", "message", at=old + dt.timedelta(days=1))
        self.assertIn("follow-up 1", report.due(self.cfg, self.c)[0][2])
        store.log_event(self.c, self.pid, "linkedin", "reply")
        self.assertEqual(report.due(self.cfg, self.c), [])


class SourceAndCliTests(Base):
    def test_parse_hn_filters_and_builds_evidence(self):
        data = {"hits": [{"title": "Show HN: Tiny DB", "author": "maya", "points": 120, "num_comments": 30,
                          "objectID": "42", "url": "https://tinydb.dev", "created_at": "2030-01-02T00:00:00Z"},
                         {"title": "Show HN: Meh", "author": "x", "points": 3, "objectID": "1"}]}
        rows = sources.parse_hn(data, 50)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["project"], "Tiny DB")
        self.assertEqual(rows[0]["evidence"], "https://news.ycombinator.com/item?id=42")

    def test_parse_github(self):
        data = {"items": [{"full_name": "acme/rocket", "html_url": "https://github.com/acme/rocket",
                           "stargazers_count": 900, "owner": {"login": "acme", "type": "Organization"},
                           "created_at": "2030-01-01T00:00:00Z", "description": "fast", "homepage": None}]}
        rows = sources.parse_github(data)
        self.assertEqual(rows[0]["handle"], "acme")
        self.assertIn("900 stars", rows[0]["signal"])

    def run_cli(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = cli.main(list(argv))
        return code, buf.getvalue()

    def test_brief_and_eml_draft(self):
        code, out = self.run_cli("brief")
        self.assertEqual(code, 0)
        self.assertIn("Next:", out)
        code, out = self.run_cli("draft", str(self.pid), "email_first", "detail=Saw the offline editor launch this week.",
                                 "--eml")
        self.assertEqual(code, 0, out)
        emls = list((self.tmp / "private" / "drafts").glob("*.eml"))
        self.assertEqual(len(emls), 1)
        self.assertIn("To: ada@example.com", emls[0].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
