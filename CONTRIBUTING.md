# Contributing to zqmlabs-software

Source for [software.zqmlabs.com](https://software.zqmlabs.com/) — the
public face of the ZQM Labs software platform: the offline-first player,
the JSON pack format, the PocketBase backend and tracker, and the Stripe
fulfillment service, plus links to the public code. The whole site is one
self-contained page, so the contribution path is short — and the
"Public code" section is a claim about the estate, so it has one rule
that matters more than the rest.

## What lives here

- `site/index.html` — the whole site (one self-contained page).
- `deploy.py` — direct-upload deploy to the Cloudflare Pages project
  `software`. Usage: `python3 deploy.py site main`.

## How to contribute

1. Fork the repo, or branch from `main` if you have write access, and
   make your edit in `site/index.html`.
2. Keep the page self-contained: this site deliberately has no build
   step and no second page. If your addition needs a full spec rather
   than a section, link out to the quest-pack spec on the quests site
   or to [docs.zqmlabs.com](https://docs.zqmlabs.com/) instead of
   growing a second page here.
3. **Only link public code in the "Public code" section.** Every repo
   linked there must be a real, public ZQM Labs repo. Never link a
   private component: the tracker is named as a component of the
   platform but is not public code, and it stays unlinked.
4. Keep dated claims dated: the "Recently shipped" list is concrete
   (what shipped, when). Add new entries with their month; don't
   quietly rewrite old entries to sound current.
5. Open a pull request against `main` describing what changed.

## Check before you open the PR

This repo has no CI workflow and no test suite, so these checks run
locally, by the author:

- Open `site/index.html` in a browser and read the changed section in
  place — layout, copy, and every link you touched.
- Confirm every link you added or changed points at a real destination
  (a public repo, the docs site, the leaders site, or the main site),
  and that no link you touched is a placeholder.

Do not deploy from a branch: deploys go through `main` via `deploy.py`
after merge.

## License

MIT — see `LICENSE`. By contributing you agree your changes are covered
by the same license.
