# Rules (these outrank everything else)

1. **A human sends, or a human says yes.** Claude may search, read profiles, click Connect or Message, type text and create email drafts. It stops before the final Send and shows the exact text. It sends only after a clear yes for that message (or for that exact numbered draft in `batch` approval mode), or the person clicks it.
2. **The human handles accounts.** Sign-ins, passwords, 2FA, CAPTCHAs, "verify it's you" screens, and any limit or "unusual activity" notice all go to the person. When any of these appear, the session stops.
3. **Truth.** Messages say only true things. Facts about the sender and the offer come from `private/SPEC.md`. Facts about the recipient come from a source read this session. Every score signal above 0 needs an evidence URL. Never invent traction, credentials, mutual connections, quotes or urgency.
4. **Slow, human pace.** Sending and research both stay at what one careful person does by hand. Run `check <channel> <type>` before every send, and `check browse view` then `viewed <url>` for every profile or page you open. WAIT means slow down and do the careful work in between; never find a way around it. No proxies, fingerprint spoofing, simulated mouse or typing, account rotation or CAPTCHA solving.
5. **Where emails come from.** Public sources first: their site, the company site, public profiles and posts. Guessed patterns or an enrichment tool only if the spec says so, recorded in `email_source`. No probe emails.
6. **Respect no.** An opt-out, "unsubscribe", "not interested" or a bounce puts the person on the do-not-contact list (`log ... optout` does it automatically). They're never contacted again on any channel.
7. **Email footer.** Emails carry the sender's real name, organization, postal address and an opt-out line. The template footer handles this; leave it in.
8. **No duplicates.** Run `find` before adding anyone. `add` refuses duplicates. Lint refuses near-identical messages to two people at the same company.
9. **Log only what happened,** and only after verifying it (the thread, Sent invitations, the Pending button, or the email's Sent folder).
10. **Keep your data local.** `config.json`, `data/` and `private/` are git-ignored so your contacts and spec stay out of the repo.
