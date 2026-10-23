# Game Library

An offline collection of **365 browser games** — a static, no-build web app.

- **GitHub repo:** https://github.com/juwpegatron/gamelib
- **Live site:** https://juwpegatron.github.io/gamelib/
- **Local source:** `C:\Users\juwen_lie\Desktop\opencode_project\GameLibrary`
- **Stack:** Static HTML/CSS/JS — one `index.html` catalog plus one file per game. No backend, no build step.
- **Assets:** `icons/` (logo + favicon), `vendor/` (three.js for 3D titles)

## What it is

`index.html` is a searchable, category-filtered catalog that links out to every
individual game page (all **relative** paths, so it works correctly on GitHub
Pages project hosting under `/gamelib/`). Games span Arcade, Puzzle, Card &
Board, Shooter, Racing, Fighting, Sports, Strategy, Sandbox, Runner, Action and
Casual categories.

## Publishing / sync

- Pushed to GitHub: `juwpegatron/gamelib`, branch `main`.
- Publishing method: GitHub Actions Pages workflow (`configure-pages` +
  `upload-pages-artifact` + `deploy-pages`).
- `.nojekyll` marker included so static files are served as-is.
- Synced: 2026-10-23.

## Notes

- Entirely client-side and offline-capable; no internet required to play once loaded.
- To update: edit files locally, then `git add -A && git commit && git push` from the
  `GameLibrary` folder; the Pages workflow redeploys automatically.
