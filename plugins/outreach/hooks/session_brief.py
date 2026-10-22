"""SessionStart: inside a paced-outreach-kit folder, show today's brief so Claude starts from the real state.

Silent everywhere else, so the plugin adds nothing to unrelated projects.
"""
import os
import subprocess
import sys
from pathlib import Path

root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
if not (root / "outreach" / "cli.py").exists():
    sys.exit(0)
if not (root / "private" / "PLAN.md").exists():
    print("[outreach] Kit found but not set up yet. Run /outreach:setup to start the interview.")
    sys.exit(0)
r = subprocess.run([sys.executable, "-m", "outreach", "brief"], cwd=root, capture_output=True, text=True,
                   encoding="utf-8", errors="replace", timeout=15)
print("[outreach] Today:\n" + (r.stdout or r.stderr).strip())
print("[outreach] Resume from private/HANDOFF.md. Check pace before every send; research slowly (check browse view).")
