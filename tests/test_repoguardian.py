import tempfile
import unittest
from pathlib import Path
from repoguardian import scan

class RepoGuardianTests(unittest.TestCase):
    def test_flags_secret_without_exposing_value(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for item in ("README.md", "LICENSE", ".gitignore"):
                (root / item).write_text("test")
            (root / "app.py").write_text('api_key = "1234567890abcdef"')
            findings = scan(root)
            self.assertTrue(any("Possible hardcoded secret" in x for x in findings))
            self.assertFalse(any("1234567890abcdef" in x for x in findings))

    def test_flags_missing_essentials(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertTrue(any("missing README.md" in x for x in scan(Path(folder))))

if __name__ == "__main__":
    unittest.main()
