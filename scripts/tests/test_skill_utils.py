from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from skill_utils import markdown_links, parse_frontmatter, parse_version, version_at_least


class SkillUtilsTests(unittest.TestCase):
    def test_parse_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text('---\nname: demo\ndescription: "A useful description"\n---\n\n# Body\n', encoding="utf-8")
            metadata, body = parse_frontmatter(path)
            self.assertEqual(metadata["name"], "demo")
            self.assertEqual(metadata["description"], "A useful description")
            self.assertEqual(body, "# Body")

    def test_version_parsing_and_order(self) -> None:
        self.assertEqual(parse_version("5.8.1"), (5, 8, 1))
        self.assertEqual(parse_version("5.8.x"), (5, 8, 0))
        self.assertTrue(version_at_least((5, 8, 1), (5, 4, 0)))
        self.assertFalse(version_at_least((5, 3, 2), (5, 4, 0)))

    def test_markdown_links(self) -> None:
        self.assertEqual(markdown_links("[one](a.md) and ![two](b.png)"), ["a.md", "b.png"])


if __name__ == "__main__":
    unittest.main()
