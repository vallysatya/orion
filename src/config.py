"""
Shared application configuration.

Loads environment variables from the project root and agent-specific .env files.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")
# Preferred location for agent secrets
load_dotenv(SRC_DIR / "agents" / "github_agent" / ".env")
# Legacy / alternate path (so edits in src/github_agent/.env still work)
load_dotenv(SRC_DIR / "github_agent" / ".env", override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_API_BASE_URL = "https://api.github.com"
APP_NAME = "orion"
DEFAULT_USER_ID = "default_user"
DEFAULT_SESSION_ID = "default_session"
