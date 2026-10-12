# Deploying the bridge

`bridge/` is served by a Cloudflare **Worker** named `firstdrop-read`, with the
custom domain `read.firstdrophq.com` bound to it.

**It is not the firstdrophq.com website.** That is a separate Cloudflare Pages
project named `firstdrophq`, built from `~/CodexProjects/claude-sessions/
terminal-logs/firstdrophq-website` on the Mac and deployed with that repo's own
`./deploy.sh`. Running that script against this directory, or this config
against that project, would overwrite a live commercial site. Keep them apart.

## From the Mac

```sh
git fetch origin claude/clickbank-product-mastery-reverse-tho7gj
git checkout claude/clickbank-product-mastery-reverse-tho7gj
cd research/clickbank-product-mastery
npx wrangler login          # only if not already authenticated
npx wrangler deploy
```

`wrangler.toml` here names the existing Worker, so this replaces its static
assets and changes nothing else. **[Likely], not verified** — this config was
written from the recorded deployment notes, not from an inspection of the
Cloudflare account. If `wrangler deploy` reports it would *create* a Worker
rather than update one, stop: the name or account is wrong, and creating a
second Worker will not serve `read.firstdrophq.com`.

## From a Claude Code session instead

A session can deploy this directly if a Cloudflare API token is stored in the
environment's settings (cloud environment menu in the title bar, then Edit)
rather than pasted into a chat. A scoped token with Workers Scripts: Edit on
this account is enough. A **new** session picks it up; the one that set it will
not.

## After any deploy

1. Open `https://read.firstdrophq.com/a/`, click the CTA.
2. Confirm it passes through `/go/a/` and lands on the ClickBank quiz.
3. Confirm the hop appears in ClickBank Analytics under `aff_sub1=a1`.
4. Repeat for `/b/` and `b1`.

If a hop does not register, the kill rule cannot be applied. Do not launch.
