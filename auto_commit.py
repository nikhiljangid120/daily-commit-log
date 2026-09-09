"""Auto-Commit Bot v2.

Appends one idempotent, timezone-aware entry per day to progress.md,
commits only that file, and pushes to origin/main.

Works in two modes:
- GitHub Actions (primary): the runner checks out a fresh copy of main,
  so the script just commits and pushes with the built-in GITHUB_TOKEN.
- Local (manual): performs a `git pull --rebase` first so local commits
  can never diverge from origin like v1 did.

Set COMMIT_TIMEZONE (IANA name) to change the day boundary; default IST.
"""

import os
import random
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

PROGRESS_FILE = "progress.md"

MESSAGES = [
    "Refining my skills one step at a time 🔁",
    "Learning something new every day 🧠",
    "Today's commit adds more value 💡",
    "Progress, not perfection 🚀",
    "Sharpening the axe before the battle ⚔️",
    "DSA problem of the day ✅",
    "Coding discipline in motion 🧘",
    "Daily log update 📓",
    "One day, one commit, closer to mastery 🌟",
]


def run(cmd: list[str]) -> None:
    """Run a git command, streaming output, failing loudly on error."""
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(f"❌ Command failed: {' '.join(cmd)}")


def today_line() -> str:
    tz = ZoneInfo(os.environ.get("COMMIT_TIMEZONE", "Asia/Kolkata"))
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d")
    return date_str, f"✅ {date_str} — {random.choice(MESSAGES)}\n"


def entry_exists(content: str, date_str: str) -> bool:
    return date_str in content


def main() -> None:
    date_str, line = today_line()

    content = ""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, encoding="utf-8") as f:
            content = f.read()

    if entry_exists(content, date_str):
        print(f"⏭️  Entry for {date_str} already exists — nothing to do.")
        return

    with open(PROGRESS_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"📝 Appended: {line.strip()}")

    # Local-mode safety net: integrate any remote commits first.
    # In CI the checkout is always fresh, so this is a fast no-op there.
    run(["git", "pull", "--rebase", "origin", "main"])

    run(["git", "add", PROGRESS_FILE])
    run(["git", "commit", "-m", f"📓 Daily log {date_str} [skip ci]"])
    run(["git", "push", "origin", "main"])
    print("🚀 Committed and pushed to origin/main.")


if __name__ == "__main__":
    main()
