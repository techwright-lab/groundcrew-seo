"""Exercise the plugin distribution commands in isolated repository copies."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class PluginPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        shutil.copytree(ROOT, self.root, symlinks=True, ignore=shutil.ignore_patterns(
            ".git", "dist", "__pycache__"))

    def run_script(self, name, *args):
        return subprocess.run(
            ["python3", str(self.root / "scripts" / name), *args],
            capture_output=True, text=True, check=False)

    def test_marketplace_generation_and_drift(self):
        result = self.run_script("generate-adapters.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        path = self.root / ".claude-plugin/marketplace.json"
        self.assertTrue(path.exists())
        marketplace = json.loads(path.read_text())
        self.assertEqual(marketplace["plugins"][0]["source"], "./")
        self.assertEqual(marketplace["plugins"][0]["name"], "groundcrew-seo")
        path.write_text("{}\n")
        result = self.run_script("generate-adapters.py", "--check")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".claude-plugin/marketplace.json", result.stderr)

    def test_zip_is_reproducible_and_contains_only_plugin_payload(self):
        result = self.run_script("build-plugin.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        archive = next((self.root / "dist").glob("*.zip"))
        original = archive.read_bytes()
        with zipfile.ZipFile(archive) as package:
            names = package.namelist()
            expected = {".codex-plugin/plugin.json", "LICENSE"}
            for folder in ("skills", "shared"):
                expected.update(str(p.relative_to(self.root))
                                for p in (self.root / folder).rglob("*")
                                if p.is_file())
            self.assertEqual(set(names), expected)
            self.assertEqual(len(names), len(set(names)))
            self.assertEqual(sum(n.endswith("/SKILL.md") for n in names), 20)
            self.assertTrue(all(info.date_time == (1980, 1, 1, 0, 0, 0)
                                for info in package.infolist()))
        for path in (self.root / "skills").rglob("*"):
            if path.is_file():
                path.touch()
        result = self.run_script("build-plugin.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(archive.read_bytes(), original)
        (self.root / "skills/private").mkdir()
        (self.root / "skills/private/secret.txt").write_text("secret")
        result = self.run_script("build-plugin.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("denied", result.stderr)
        self.assertEqual(archive.read_bytes(), original)

    def test_zip_rejects_symlinks_and_mcp_configuration(self):
        (self.root / "shared/leak").symlink_to(self.root / "install.sh")
        result = self.run_script("build-plugin.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("symlink", result.stderr)
        (self.root / "shared/leak").unlink()
        (self.root / "shared/.mcp.json").write_text("{}")
        result = self.run_script("build-plugin.py")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("denied", result.stderr)


if __name__ == "__main__":
    unittest.main()
