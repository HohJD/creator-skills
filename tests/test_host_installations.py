"""Exercise installed packages as a consumer, outside the source checkout."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("installer", ROOT / "tools/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def contents(folder):
    return {
        p.relative_to(folder): p.read_bytes()
        for p in folder.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    }


class HostInstallations(unittest.TestCase):
    def test_consumer_installations(self):
        for agent, relative in (("codex", ".agents/skills"), ("claude", ".claude/skills")):
            for scope in ("user", "project"):
                with self.subTest(agent=agent, scope=scope), tempfile.TemporaryDirectory() as tmp:
                    user = Path(tmp) / "test user"
                    project = Path(tmp) / "sample project"
                    project.mkdir()
                    with patch.object(Path, "home", return_value=user):
                        installer.install(agent, scope, project)
                    installed = (user if scope == "user" else project) / relative
                    self.assertEqual(contents(installed), contents(ROOT / "content-creation"))
                    (project / "cues.json").write_text(json.dumps([
                        {"start_ms": 100, "end_ms": 1200, "text": "Look here."}
                    ]), encoding="utf-8")
                    track = subprocess.check_output([
                        sys.executable, installed / "subtitle-editor/scripts/export_captions.py",
                        "cues.json", "--format", "vtt",
                    ], cwd=project, text=True)
                    self.assertIn("00:00:00.100 --> 00:00:01.200\nLook here.", track)
                    url = subprocess.check_output([
                        sys.executable, installed / "campaign-links/scripts/tag_url.py",
                        "https://example.org/#note", "--source", "studio",
                        "--medium", "email", "--campaign", "launch",
                    ], cwd=project, text=True)
                    self.assertEqual(url.strip(), "https://example.org/?utm_source=studio"
                                     "&utm_medium=email&utm_campaign=launch#note")

    def test_updated_skill_has_only_one_discoverable_copy(self):
        for agent in ("codex", "claude"):
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)
                skill, = installer.install(agent, "project", project, skill="social-captions")
                (skill / "SKILL.md").write_text("My local edits", encoding="utf-8")
                installer.install(agent, "project", project, skill=skill.name, force=True)
                self.assertEqual(list(skill.parent.rglob("SKILL.md")), [skill / "SKILL.md"])
                archive = skill.parent.parent / "creator-skills-backups"
                backup, = archive.rglob("SKILL.md")
                self.assertEqual(backup.read_text(encoding="utf-8"), "My local edits")
                self.assertEqual(contents(skill), contents(ROOT / "content-creation" / skill.name))
