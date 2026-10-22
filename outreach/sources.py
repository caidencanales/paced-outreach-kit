"""Built-in public sources for finding candidates. Free APIs, no keys, no logins.

    python -m outreach source hn [--days 14] [--min-points 50] [--out private/candidates/hn.csv]
    python -m outreach source github [--days 60] [--min-stars 300] [--query "topic:ai"] [--out ...]

Output is a candidates CSV (not people yet): who built it, what, the evidence URL and the signal. Claude then finds
the founder's real name, LinkedIn and email, scores them, and adds the good ones with `import` or `add`.
Set GITHUB_TOKEN to raise GitHub's rate limit (optional).
"""
import csv
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

UA = {"User-Agent": "paced-outreach-kit"}
FIELDS = ["source", "handle", "project", "project_url", "homepage", "signal", "evidence", "created", "about"]


def _get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def parse_hn(data, min_points):
    out = []
    for h in data.get("hits", []):
        if (h.get("points") or 0) < min_points:
            continue
        title = (h.get("title") or "").removeprefix("Show HN:").strip()
        out.append({"source": "Show HN", "handle": h.get("author", ""), "project": title,
                    "project_url": h.get("url") or "", "homepage": h.get("url") or "",
                    "signal": f"{h.get('points', 0)} points, {h.get('num_comments', 0)} comments",
                    "evidence": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                    "created": (h.get("created_at") or "")[:10], "about": title})
    return out


def hn(days=14, min_points=50):
    since = int((dt.datetime.now() - dt.timedelta(days=days)).timestamp())
    rows, page = [], 0
    while page < 5:
        q = urllib.parse.urlencode({"tags": "show_hn", "numericFilters": f"created_at_i>{since},points>={min_points}",
                                    "hitsPerPage": 100, "page": page})
        data = _get("https://hn.algolia.com/api/v1/search?" + q)
        rows += parse_hn(data, min_points)
        page += 1
        if page >= data.get("nbPages", 0):
            break
    return rows


def parse_github(data):
    out = []
    for r in data.get("items", []):
        owner = r.get("owner") or {}
        out.append({"source": "GitHub", "handle": owner.get("login", ""), "project": r.get("full_name", ""),
                    "project_url": r.get("html_url", ""), "homepage": r.get("homepage") or "",
                    "signal": f"{r.get('stargazers_count', 0)} stars, {owner.get('type', '')} owner",
                    "evidence": r.get("html_url", ""), "created": (r.get("created_at") or "")[:10],
                    "about": (r.get("description") or "")[:200]})
    return out


def github(days=60, min_stars=300, query=""):
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    q = f"created:>{since} stars:>={min_stars} {query}".strip()
    headers = {"Accept": "application/vnd.github+json"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": q, "sort": "stars", "order": "desc", "per_page": 100})
    return parse_github(_get(url, headers))


def write(rows, out):
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    return out
