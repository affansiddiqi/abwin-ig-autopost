# ABWIN Instagram Autopost

Posts one image + caption from `queue.json` to Instagram every 3 hours via GitHub Actions —
runs entirely in the cloud, independent of any local machine being on.

## How it works

- `images/` — 37 posts, converted to Instagram-compliant JPEGs (≤8MB, ~4:5 portrait).
- `queue.json` — ordered list of posts with pre-written captions. Each post has `posted`/`posted_at`
  fields; the poster script finds the next unposted item, posts it, marks it posted, and commits
  the updated file back to the repo. When every item has been posted once, the queue automatically
  resets so posting continues indefinitely.
- `.github/workflows/post.yml` — runs `scripts/post.py` every 3 hours (`0 */3 * * *`), and can also
  be triggered manually from the Actions tab ("Run workflow") to test or force a post immediately.
- `scripts/post.py` — calls the Instagram Graph API's Content Publishing endpoints:
  1. `POST /{ig-user-id}/media` with the image's raw GitHub URL + caption (creates a container)
  2. Polls the container until `status_code` is `FINISHED`
  3. `POST /{ig-user-id}/media_publish` to actually publish it

Images are served to Instagram via `https://raw.githubusercontent.com/<owner>/<repo>/main/images/<file>`,
which requires this repository to be **public** (Instagram's servers must be able to fetch the URL
with no auth).

## One-time setup (do this yourself — see note below)

This repo needs two **GitHub Actions secrets**. Add them at:
**Repo → Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Value |
|---|---|
| `IG_ACCESS_TOKEN` | A valid Meta Graph API access token with `instagram_content_publish`, `instagram_basic`, and `pages_show_list` permissions for the Abwin Labs Instagram Business account. |
| `IG_USER_ID` | `17841469660999692` (Abwin Labs' Instagram Business Account ID — already looked up, not sensitive, but kept as a secret for tidiness). |

**Important — about the access token:**
- Do not paste tokens into chat with an AI assistant, or anywhere else outside a proper secret
  store — it's the same as a password. Add it directly into GitHub's secret field yourself.
- A plain user access token from Graph API Explorer expires quickly (short-lived: ~1-2 hours,
  long-lived: ~60 days). For an automation meant to run unattended indefinitely, you'll need to
  either:
  - Manually refresh `IG_ACCESS_TOKEN` every ~60 days (exchange for a new long-lived token via
    `GET /oauth/access_token?grant_type=fb_exchange_token&...` and update the GitHub secret), or
  - Set up a Meta **System User** token in Business Manager, which can be issued without an
    expiration and is the standard approach for unattended server-to-server automations.
- If the automation starts failing with an authentication error in the Actions log, this is almost
  always why — go refresh the token.

## Manual test

From the Actions tab, run the "Post to Instagram" workflow manually (`workflow_dispatch`) once
secrets are set, to confirm the first post goes through before waiting for the schedule.

## Editing captions or order

Edit `queue.json` directly (any text editor, or re-run `scripts/build_queue.py` after editing it
to regenerate from scratch — note that will reset all `posted` flags). Reorder, tweak captions, or
add new entries any time; the poster always just takes the next unposted item top-to-bottom.
