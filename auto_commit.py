import os
from datetime import datetime
import random

# Motivational commit messages
messages = [
    "Refining my skills one step at a time 🔁",
    "Learning something new every day 🧠",
    "Today's commit adds more value 💡",
    "Progress, not perfection 🚀",
    "Sharpening the axe before the battle ⚔️",
    "DSA problem of the day ✅",
    "Coding discipline in motion 🧘",
    "Daily log update 📓",
    "One day, one commit, closer to mastery 🌟"
]

# Append a new line to progress.md with timestamp and message
msg = random.choice(messages)
log_line = f"✅ {msg} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
with open("progress.md", "a") as file:
    file.write(log_line)

# Git commands to commit and push
os.system("git add .")
os.system(f'git commit -m "{msg}"')
os.system("git push origin main")
