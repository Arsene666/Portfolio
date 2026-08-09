"""Seed the database with Arsène Godonou's real projects.

Usage:
    python scripts/seed_projects.py

Note: the app now also runs this automatically on startup (see
app/main.py), since Render's free tier doesn't persist the local SQLite
file across restarts. This script is still useful for local development
and for re-seeding manually after editing app/db/seed.py.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db.seed import seed  # noqa: E402

if __name__ == "__main__":
    seed()
    print("Done.")