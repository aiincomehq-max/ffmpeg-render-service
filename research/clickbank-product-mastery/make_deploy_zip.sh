#!/bin/sh
# Builds firstdrop-read-deploy.zip: the bridge assets plus the Worker config,
# and nothing else. Used when the Mac cannot reach GitHub and the package has
# to be handed over directly.
#
# The output is a build artifact and is deliberately NOT committed. Two copies
# of bridge/ in the repository is how you end up deploying the wrong one.
set -e
cd "$(dirname "$0")"
OUT=firstdrop-read-deploy
rm -rf "$OUT" "$OUT.zip"
mkdir -p "$OUT"
cp -a bridge "$OUT/bridge"
cp wrangler.toml DEPLOY.md "$OUT/"

cat > "$OUT/README-DEPLOY-FIRST.txt" <<TXT
firstdrop-read - bridge deploy package
Generated $(date -u +%Y-%m-%d) from $(git rev-parse --abbrev-ref HEAD) @ $(git rev-parse --short HEAD)

WHAT THIS IS
  Static assets for the Cloudflare Worker "firstdrop-read", serving
  read.firstdrophq.com. Carries the Taboola pixel (account 2125039) and the
  offer_click handler.

WHAT THIS IS NOT
  NOT the firstdrophq.com website. That is a separate Cloudflare Pages project
  named "firstdrophq". Never deploy this against it.

TO DEPLOY
  1. Unzip anywhere on the Mac.
  2. cd into the unzipped folder (the one holding wrangler.toml).
  3. npx wrangler login      # only if not already authenticated
  4. npx wrangler deploy

  STOP if wrangler says it would CREATE a Worker rather than update
  "firstdrop-read". That means the wrong Cloudflare account is authenticated,
  and a new Worker will not serve read.firstdrophq.com.

TO VERIFY AFTERWARDS
  curl -s https://read.firstdrophq.com/a/ | grep -c tb_tfa_script   # expect 1
  curl -s https://read.firstdrophq.com/b/ | grep -c tb_tfa_script   # expect 1
  Then open /a/ and click the CTA; it must reach the ClickBank offer page.

No GitHub access is needed for any of the above.
TXT

zip -qr "$OUT.zip" "$OUT"
rm -rf "$OUT"
echo "built $OUT.zip"
sha256sum bridge/a/index.html bridge/b/index.html
