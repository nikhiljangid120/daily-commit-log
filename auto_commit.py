"""Auto-Commit Bot v2.

Appends one idempotent, timezone-aware entry per day to progress.md,
commits only that file, and pushes to origin/main.

Works in two modes:
- GitHub Actions (primary): the runner checks out a fresh copy of main,
  so the script just commits and pushes with the built-in GITHUB_TOKEN.
- Local (manual): performs a `git pull --rebase` on the clean tree first
  so local commits can never diverge from origin like v1 did.

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


class GitError(RuntimeError):
    """A git command failed."""


def configure_streams() -> None:
    """Emoji-rich output must not crash on Windows cp1252 consoles."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def run(cmd: list[str]) -> None:
    """Run a git command, failing loudly (non-zero exit) on error."""
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise GitError(f"Command failed: {' '.join(cmd)}")


def today_entry() -> tuple[str, str]:
    tz = ZoneInfo(os.environ.get("COMMIT_TIMEZONE", "Asia/Kolkata"))
    date_str = datetime.now(tz).strftime("%Y-%m-%d")
    return date_str, f"✅ {date_str} — {random.choice(MESSAGES)}\n"


def read_progress() -> str:
    if not os.path.exists(PROGRESS_FILE):
        return ""
    with open(PROGRESS_FILE, encoding="utf-8") as f:
        return f.read()


def has_entry(content: str, date_str: str) -> bool:
    return date_str in content


def sync_with_remote() -> None:
    """Local-mode safety net: integrate remote commits while the tree is
    still clean. In CI the checkout is always fresh, so skip it there."""
    if os.environ.get("GITHUB_ACTIONS") == "true":
        return
    run(["git", "pull", "--rebase", "origin", "main"])


def main() -> None:
    configure_streams()
    date_str, line = today_entry()

    if has_entry(read_progress(), date_str):
        print(f"⏭️  Entry for {date_str} already exists — nothing to do.")
        return

    sync_with_remote()

    # The pull may have brought in today's entry (e.g. Actions ran first).
    if has_entry(read_progress(), date_str):
        print(f"⏭️  Remote already has the {date_str} entry — nothing to do.")
        return

    with open(PROGRESS_FILE, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"📝 Appended: {line.strip()}")

    run(["git", "add", PROGRESS_FILE])
    run(["git", "commit", "-m", f"📓 Daily log {date_str} [skip ci]"])

    try:
        run(["git", "push", "origin", "main"])
    except GitError:
        # Remote may have moved between pull and push; rebase and retry once.
        print("⚠️  Push rejected — rebasing on latest origin/main and retrying…")
        run(["git", "pull", "--rebase", "origin", "main"])
        run(["git", "push", "origin", "main"])

    print("🚀 Committed and pushed to origin/main.")


if __name__ == "__main__":
    main()
