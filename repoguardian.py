"""RepoGuardian: basic offline repository hygiene scanner."""
from __future__ import annotations
import argparse
from pathlib import Path
import re

SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
PATTERNS = [
    ("Possible private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Possible hardcoded secret", re.compile(r"""(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\s*[:=]\s*['"][^'"]{8,}['"]""")),
]
MAX_BYTES = 512_000

def scan(root: Path) -> list[str]:
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Expected a directory")
    findings = []
    for essential in ("README.md", "LICENSE", ".gitignore"):
        if not (root / essential).is_file():
            findings.append(f"Project hygiene: missing {essential}")
    for file in sorted(root.rglob("*")):
        if file.is_symlink() or not file.is_file():
            continue
        relative = file.relative_to(root)
        if any(part in SKIP for part in relative.parts) or any(part.startswith(".") for part in relative.parts[:-1]):
            continue
        try:
            if file.stat().st_size > MAX_BYTES:
                continue
            data = file.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        for number, line in enumerate(data.splitlines(), start=1):
            for title, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(f"{relative.as_posix()}:{number}: {title} (value redacted)")
    return findings

def main() -> None:
    parser = argparse.ArgumentParser(description="Scan local project for basic repo hygiene and potential secrets")
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    try:
        findings = scan(args.project)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if findings:
        for finding in findings:
            print(finding)
        raise SystemExit(1)
    print("No issues detected by these limited checks. Manual review is still necessary.")

if __name__ == "__main__":
    main()
