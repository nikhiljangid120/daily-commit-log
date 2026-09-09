# 🤖 GitHub Auto-Commit Bot v2

A **daily-commit bot that runs entirely on GitHub Actions** — no local scheduler, no personal access token, no "my PC was off so the streak broke". Every day at **09:00 IST**, a workflow appends one dated entry to `progress.md`, commits it, and pushes to `main`.

> v1 ran locally via Task Scheduler/cron and broke the moment the branch diverged or the machine was off. v2 runs in the cloud and is structurally immune to both.

## 📦 What v2 does

- **Runs on GitHub's schedule** — cron `30 3 * * *` UTC = 09:00 IST daily (GitHub may start runs up to ~30–60 min late; that's normal).
- **Commits unconditionally** — one entry per day, keeping the streak alive.
- **Idempotent** — if today's entry already exists, the run skips instead of duplicating. Safe for manual re-runs and retries.
- **Timezone-aware** — day boundary is IST (`Asia/Kolkata`), not the runner's UTC. Change via the `COMMIT_TIMEZONE` env var.
- **Safe git hygiene** — commits *only* `progress.md` (never `git add .`), runs `git pull --rebase` before pushing in local mode, and marks commits `[skip ci]` to prevent workflow loops.
- **Loud failures** — any git error exits non-zero so the Actions run shows red instead of failing silently (v1's biggest flaw).
- **No PAT needed** — uses Actions' built-in `GITHUB_TOKEN` with scoped `contents: write` permission.

## 🚀 Usage

### Automatic (default)
Once this workflow is on `main`, it just runs. Nothing to install, nothing to schedule.

### Manual trigger
GitHub repo → **Actions** → *Daily auto-commit* → **Run workflow**. Useful right after setup to verify everything works, or to catch up a missed day.

### Local run (optional)
```bash
python auto_commit.py
```
Appends today's entry, rebases on `origin/main`, commits, and pushes using your local git credentials.

## ⚠️ Two things to know

1. **Scheduled workflows auto-pause after 60 days** if the repo has no activity. A fix: bump the default branch or re-enable from the Actions tab. (The bot's own daily commits count as activity, so this rarely triggers.)
2. **Contribution graph visibility** — if this repo is private, enable **Private contributions** in your GitHub profile settings for the commits to show.

## 🗺️ Roadmap

- [ ] Streak counter in the commit message
- [ ] Weekend-specific messages
- [ ] Retry slot (second cron) for missed runs

## ⚠️ Disclaimer
Use this tool responsibly. This is meant to reflect real daily progress or logs. Avoid using it to fake activity with no real value.
