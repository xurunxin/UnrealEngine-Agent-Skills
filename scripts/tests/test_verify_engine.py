from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from verify_engine import engine_version, normalize_root


class VerifyEngineTests(unittest.TestCase):
    def test_normalize_and_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "Engine" / "Build"
            path.mkdir(parents=True)
            (path / "Build.version").write_text(
                json.dumps({"MajorVersion": 5, "MinorVersion": 8, "PatchVersion": 1}),
                encoding="utf-8",
            )
            self.assertEqual(normalize_root(root), root.resolve())
            version, _ = engine_version(root)
            self.assertEqual(version, (5, 8, 1))


if __name__ == "__main__":
    unittest.main()
