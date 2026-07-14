from pathlib import Path

from dotenv import dotenv_values

p = Path("src/agents/github_agent/.env")
raw = p.read_bytes()
print("file starts with BOM:", raw[:3] == b"\xef\xbb\xbf")
print("file size:", len(raw))
vals = dotenv_values(p)
for key in ("GOOGLE_API_KEY", "GITHUB_TOKEN"):
    value = vals.get(key) or ""
    starts_aiza = value.startswith("AIza") if key == "GOOGLE_API_KEY" else "n/a"
    print(
        f"{key}: present={bool(value)} len={len(value)} "
        f"starts_with_AIza={starts_aiza} has_whitespace={value != value.strip()}"
    )
