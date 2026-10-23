# zqmlabs-software

Source for **software.zqmlabs.com** — the public face of the ZQM Labs
software platform: the offline-first player, the JSON pack format, the
PocketBase backend and tracker, and the Stripe fulfillment service,
plus links to the public code.

## Layout

- `site/index.html` — the whole site (one self-contained page).
- `deploy.py` — direct-upload deploy to the Cloudflare Pages project
  `software` (the estate's pattern: production builds are direct-upload,
  not git-connected). Usage: `python3 deploy.py site main`.

## History

Stood up 2026-10-23 as a focused-content host (it previously mirrored
the apex site), scoped to ZQM Labs' own software. Repo created the same
day at Alex's direction so the source survives any single machine.
