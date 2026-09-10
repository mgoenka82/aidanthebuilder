# Legos for Aidan 🧱

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
read. Then commit and push; DigitalOcean App Platform redeploys on its own.

Check it first:

```sh
python3 scripts/check-videos.py
```

## On the iPad

Open the site in Safari, then **Share → Add to Home Screen**. It launches
full-screen with no address bar, so there is nothing to tap out of.
