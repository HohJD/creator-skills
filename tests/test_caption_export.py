import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "content-creation/subtitle-editor/scripts/export_captions.py"


class ExportCaptionsTests(unittest.TestCase):
    def export(self, path, fmt):
        return subprocess.run(
            [sys.executable, str(EXPORT), str(path), "--format", fmt],
            capture_output=True,
        )

    def test_published_tracks_match_the_example_data(self):
        examples = ROOT / "examples/creator-captions"
        for fmt in ("srt", "vtt"):
            with self.subTest(fmt=fmt):
                result = self.export(examples / "cues.json", fmt)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, (examples / f"example.{fmt}").read_bytes())

    def test_overlap_unicode_and_markup_in_vtt(self):
        cues = [
            {"start_ms": 3599999, "end_ms": 3601200, "text": "Jo: A & B"},
            {"start_ms": 3600000, "end_ms": 3600300, "text": "北京 < 3"},
        ]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "cues.json"
            path.write_text(json.dumps(cues), encoding="utf-8")
            result = self.export(path, "vtt")
        self.assertEqual(result.returncode, 0, result.stderr)
        track = result.stdout.decode("utf-8")
        self.assertIn("00:59:59.999 --> 01:00:01.200", track)
        self.assertIn("A &amp; B", track)
        self.assertIn("北京 &lt; 3", track)

    def test_invalid_later_cue_emits_no_partial_track(self):
        first = {"start_ms": 100, "end_ms": 200, "text": "First"}
        for changes in ({"start_ms": 10}, {"end_ms": 100}, {"start_ms": True},
                        {"text": "a\n\nb"}, {"text": None}):
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as td:
                path = Path(td) / "cues.json"
                path.write_text(json.dumps([first, {**first, **changes}]), encoding="utf-8")
                result = self.export(path, "srt")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
                self.assertIn(b"cue 2", result.stderr)


if __name__ == "__main__":
    unittest.main()
