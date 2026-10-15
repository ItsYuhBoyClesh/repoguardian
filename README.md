# RepoGuardian

A lightweight, offline Python scanner for common repository hygiene issues and potential hardcoded secrets.

**An Open Heightz initiative founded by Clesh TN Maluleka.**

## Quick start
Requires Python 3.10+; no third-party dependencies.

```bash
python repoguardian.py path/to/project
python -m unittest discover -s tests
```

The scanner checks files for suspicious credential assignments and private-key headers, and flags missing README, LICENSE and .gitignore. It ignores common generated directories, hidden files, and symlinks. It **never** uploads project contents.

## Limitations
Regex checks can produce false positives and miss secrets. This is not a complete security audit, and it cannot check Git history or confirm that credentials have been revoked. Treat findings as prompts for manual review. If a real secret is exposed, revoke and rotate it promptly.

## Community
Read [CONTRIBUTING.md](CONTRIBUTING.md), [AUTHORS.md](AUTHORS.md), [SECURITY.md](SECURITY.md), and [NOTICE.md](NOTICE.md). MIT licensed.