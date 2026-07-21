"""Console-safe status markers for the Orion CLI."""

from __future__ import annotations

import sys


def _can_encode(text: str) -> bool:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        text.encode(encoding)
        return True
    except (LookupError, UnicodeEncodeError):
        return False


def ok_mark() -> str:
    return "✓" if _can_encode("✓") else "OK"


def fail_mark() -> str:
    return "✗" if _can_encode("✗") else "X"


def pass_mark() -> str:
    return "✔" if _can_encode("✔") else "PASS"


def bullet() -> str:
    return "•" if _can_encode("•") else "-"


def configure_stdout() -> None:
    """Prefer UTF-8 on Windows consoles when the stream supports it."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError, AttributeError):
                pass
