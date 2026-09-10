# Aidan the Builder 🧱

A deliberately simple website so a five-year-old can find a new thing to build
out of the LEGO bricks he already has: pick a theme, pick a build, watch it.

Themes: space, cars, trains, robots, Titanic.

## How it works

- `index.html` — the whole site. One file, no build step, no dependencies.
  The `THEMES` table near the bottom of the file is the only thing to edit.
- The videos are **other people's YouTube tutorials**, embedded through
  `youtube-nocookie.com` with related videos and autoplay-to-next turned off,
  so a video ends back on this page instead of in YouTube's recommendations.
- `scripts/check-videos.py` verifies every embedded video is still playable.
  A GitHub Action runs it weekly (see `.github/workflows/check-videos.yml`).

## Adding a build

Add an entry to the right theme in `THEMES` in `index.html`:

```js
{ id:"YOUTUBE_VIDEO_ID", label:"Short Name", who:"Channel Name" },
```

Keep `label` to two words — it is read by someone who is still learning to
read. Then check it and ship it:

```sh
python3 scripts/check-videos.py    # are the embeds all playable?
git commit -am "add a build" && git push
./deploy.sh                        # push alone does NOT redeploy
```

The app is deployed from this repo's public clone URL, which App Platform
serves without a webhook — so a push updates GitHub but not the live site.
`deploy.sh` triggers the deploy and waits for it.

## The site

<https://aidan.mg82.org>

A subdomain of a domain that was already owned, so it costs nothing. DNS lives
at Cloudflare: a single `CNAME aidan -> aidanthebuilder-tetyi.ondigitalocean.app`,
deliberately **not proxied** (grey cloud). Cloudflare's proxy would intercept
Let's Encrypt validation and DigitalOcean's certificate would never renew.

## On the iPad

Open the site in Safari, then **Share → Add to Home Screen**. It launches
full-screen with no address bar, so there is nothing to tap out of.

## Why the player is built the way it is

The embed is driven through the YouTube IFrame API with `controls: 0`, a
transparent shield over the player, and our own buttons below it. That is
deliberate: YouTube's own player makes the title and logo tappable links out
to youtube.com, and fills the frame with recommended videos when one ends. A
five-year-old finds both immediately. On `ENDED` we stop the player and cover
it with our own panel, so the recommendation grid is never rendered.

Ads inside the embed cannot be removed, and the YouTube wordmark may flash
while a video loads. Those are the terms of using their player.
