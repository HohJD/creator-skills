import subprocess
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "content-creation/campaign-links/scripts/tag_url.py"


def run(url, *extra):
    return subprocess.run([sys.executable, str(SCRIPT), url, "--source", "digest",
                           "--medium", "email", "--campaign", "repair", *extra],
                          text=True, capture_output=True)


class CampaignLinks(unittest.TestCase):
    def test_preserves_original_parameters_and_is_idempotent(self):
        old = "https://example.org/guide?lang=en&sort=a%20b&key=1&key=2&utm_source=digest#tools"
        out = run(old, "--content", "café & clip")
        self.assertEqual(out.returncode, 0, out.stderr)
        result = out.stdout.strip()
        self.assertTrue(result.startswith(old.split("#")[0] + "&"))
        self.assertEqual(urlsplit(result).fragment, "tools")
        self.assertEqual(parse_qs(urlsplit(result).query)["utm_content"], ["café & clip"])
        self.assertEqual(run(result, "--content", "café & clip").stdout.strip(), result)

    def test_conflicts_and_signed_destinations_produce_no_link(self):
        for query in ("utm_campaign=other", "utm_source=digest&utm_source=digest",
                      "%75tm_campaign=other", "UTM_campaign=repair", "X-Amz-Signature=abc"):
            with self.subTest(query=query):
                result = run("https://example.org/path?" + query)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
