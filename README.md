# zqmlabs-software

Source for **software.zqmlabs.com**, the ZQM Labs software-platform overview for its offline-first quest player, JSON quest-pack format, PocketBase-backed services, event tracker, and Stripe fulfillment flow. This repository is a public information site and deploy script, not proof that every linked service or paid order path is production-ready; confirm each service's live status and end-to-end fulfillment evidence separately.

## Layout

- `site/index.html` — the whole site (one self-contained page).
- `deploy.py` — direct-upload deploy to the Cloudflare Pages project
  `software` (the estate's pattern: production builds are direct-upload,
  not git-connected). Usage: `python3 deploy.py site main`.

## History

Stood up 2026-10-23 as a focused-content host (it previously mirrored
the apex site), scoped to ZQM Labs' own software. Repo created the same
day at Alex's direction so the source survives any single machine.
