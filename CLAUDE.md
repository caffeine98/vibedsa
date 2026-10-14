# VibeDSA

A data structures and algorithms reference for people who already code.
Astro + Starlight static site, deployed to GitHub Pages at https://caffeine98.github.io/vibedsa/.

**Read `STYLE.md` before writing or editing any lesson.** Simple, short, plain English is the main goal.

## Layout
- `src/content/docs/<section>/<topic>.mdx` — lesson pages.
- `python/dsa/<topic>.py` — lesson code. Shown in full on the page, so keep it clean.
- `python/tests/test_<topic>.py` — pytest tests for that module.
- `src/data/curriculum.mjs` — the full topic list and order. Drives the home index and the sidebar.
  A topic appears in the sidebar as soon as its `.mdx` file exists.
- `src/styles/theme.css` — the theme (dark "blueprint", light "notebook"). Square corners, no gradients, no shadows.
- `src/components/` — `Hero.astro` (home only), `Curriculum.astro` (home index).

## Showing Python in a lesson
```mdx
import { Code } from '@astrojs/starlight/components';
import src from '../../../../python/dsa/binary_search.py?raw';

<Code code={src} lang="python" title="binary_search.py" />
```

## Workflow for a new topic
1. Write `python/dsa/<topic>.py` and its tests. Run `.venv/Scripts/python -m pytest` until green.
2. Write the `.mdx` page following `STYLE.md`.
3. Run `npm run build` and check the page.
4. The user reviews for simplicity before it is merged.

## Git
Never run git write actions (commit, push, branch, merge, tag, stash, etc.). The user does all git actions themselves.
Read-only commands like `git status`, `git diff` and `git log` are fine.

## Commands
- Dev server: `npx astro dev --background` (manage with `astro dev stop|status|logs`).
- Build: `npm run build`. Tests: `.venv/Scripts/python -m pytest`.
- CI (`.github/workflows/deploy.yml`) runs pytest, then builds, then deploys. Failing tests block the deploy.
