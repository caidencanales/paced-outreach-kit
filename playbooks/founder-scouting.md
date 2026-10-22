# Playbook: scouting exceptional early founders and inviting them to apply

**Goal:** find founders who could plausibly build the next big company, ideally ones who also build in public on social media. Find their LinkedIn, find a public email, and invite them to apply to your program (a fund, fellowship, accelerator, community or event). Setup customizes this into `private/PLAYBOOK.md`.

## 1. Who counts
Defaults (the interview replaces them):
- **Stage:** pre-seed to Series A, company under 3 years old, team under 25.
- **Must-have:** at least one strong signal from section 3 backed by evidence.
- **Social presence:** preferred, not required. A founder with no audience but great traction still qualifies. A big audience alone doesn't.
- **Red flags:** no real product, claims you can't verify anywhere, engagement-bait content with no substance, prior conduct issues in reputable press, and anyone the spec puts off-limits.

## 2. Where to look (public sources; confirm which ones in setup)
- **Launches:** Product Hunt (daily top), Hacker News "Show HN", GitHub trending and fast-growing repos, App Store or Play "new and rising" in your category.
- **Selection signals:** accelerator batches and demo days (public company directories), fellowships, university venture programs, pitch competition winners.
- **Build-in-public founders:** X/Twitter, LinkedIn posts, YouTube, TikTok, Instagram and Substack founders who share metrics or progress.
- **Press and data:** TechCrunch and newsletter funding roundups, public Crunchbase pages, company blogs and changelogs, job boards (hiring velocity).
- **Your network:** who your best founders recommend.

Log the source on every person (`"source": "Show HN 2030-01-14"`). After a few weeks, `report` tells you which sources produce replies.

## 3. Scoring (signals map to `config.json` → `scoring.signals`)
Score each 0-5 and attach the URL you read. With no URL, the signal stays 0.

| Signal | 1 | 3 | 5 |
|---|---|---|---|
| `founder_track_record` | first-time founder, relevant job | shipped notable product, or a senior role at a strong company | prior exit, or a breakout prior company |
| `technical_or_domain_depth` | adjacent experience | built the core tech, or years in the domain | recognized expert: research, patents, a famous open-source project |
| `traction` | waitlist | paying users or clear organic growth | strong revenue or usage growth with public numbers |
| `velocity` | occasional updates | ships every week or two | visible weekly progress, fast hiring |
| `market_size` | niche | large niche | huge or new category |
| `backing_or_selection` | none | angels, or a competitive program | top-tier accelerator or a known lead investor |
| `social_audience` | under 1k engaged followers | 1k–20k with real engagement | 20k+ engaged, or a breakout post |
| `social_consistency` | sporadic | posts weekly | posts multiple times a week with substance |

```
python -m outreach score <ref> '{"traction": {"value": 4, "evidence": "https://...", "why": "public MRR chart"}, ...}'
```

Contact anyone at or above `min_score_to_contact` (default 60). Borderline cases go to the person for review.

## 4. Finding the founder's LinkedIn
1. Get the company's About or Team page, and the founder's name exactly as written there.
2. Search LinkedIn people for "<name> <company>", or open the company page's People tab.
3. Confirm the match: current title says founder or CEO at that company, and the photo or bio matches the company site. If it's ambiguous, skip.
4. Save the canonical URL (`https://www.linkedin.com/in/<slug>`).

## 5. Finding a public email (in this order, stop at the first hit)
1. An email the founder publishes: personal site, newsletter, a post saying "email me at".
2. The company site's contact, team or press page (`founders@`, `hello@` are fine).
3. The public contact field on their profile pages (GitHub profile, YC-style directory pages, their X bio link).
4. **Only if the spec allows it:** a guessed pattern (`first@domain`), recorded as `email_source: guessed`. Never verified with probe emails.
5. Nothing found: use LinkedIn only.

Record where it came from: `"email_source": "company team page https://..."`.

## 6. Default sequence (setup can change it)
- **Day 0:** LinkedIn connection request. A note goes to founders scoring 75+ (if you have the note budget); everyone else gets a bare request.
- **Day 0–1:** cold email with the invite to apply (`templates/email_first.md`).
- **On accept:** a LinkedIn message only if they haven't replied to the email; never the same text.
- **Day +4 business days, no reply:** one email follow-up with something new (a new detail, the deadline).
- **Then stop.** No reply after the follow-up means no.

## 7. What a good message does
- Opens with the one true, specific thing you noticed (`{detail}`): their launch, a metric they shared, a post you actually read.
- Says in one sentence what the program gives them, not what it is.
- Asks for one thing: apply (with the link), or a 15-minute call.
- Stays under 120 words for email and 200 characters for a note.

Example shape (templates hold the real wording):
> Hi Maya! Your Show HN for the offline-first notes app was the cleanest launch I've seen this month. I help run {program_name}, {program_one_liner} I think you'd be a great fit, and applications close Friday: {apply_url}
