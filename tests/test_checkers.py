import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "content-creation"
LINT = ROOT / "tools/creator_lint.py"


def load(relative):
    spec = importlib.util.spec_from_file_location(Path(relative).stem, SKILLS / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


subs = load("subtitle-editor/scripts/lint_captions.py")
post = load("social-captions/scripts/check_post.py")
alt = load("image-descriptions/scripts/check_alt.py")
loc = load("content-localization/scripts/compare_versions.py")


def codes(findings):
    return [f["code"] for f in findings]


class SubtitleLintTests(unittest.TestCase):
    def test_the_published_examples_are_clean(self):
        for name in ("example.srt", "example.vtt", "cues.json"):
            with self.subTest(name=name):
                text = (ROOT / "examples/creator-captions" / name).read_text(encoding="utf-8")
                self.assertEqual(subs.check(subs.parse(text)), [])

    def test_each_rule_fires_on_the_cue_that_breaks_it(self):
        track = ("1\n00:00:01,000 --> 00:00:01,400\n" + "x" * 50 + "\nb\nc\n\n"
                 "2\n00:00:01,200 --> 00:00:00,900\n\n\n"
                 "3\n00:00:0x --> bad\nhi\n\n"
                 "4\n00:00:00,500 --> 00:00:09,000\nLong on screen\n")
        found = subs.check(subs.parse(track))
        self.assertEqual(codes(found), ["SUB101", "SUB102", "SUB103", "SUB105", "SUB004", "SUB002", "SUB005",
                                        "SUB001", "SUB003", "SUB104"])
        self.assertEqual(found[0]["line"], 2)

    def test_vtt_tags_settings_and_notes_are_not_text(self):
        track = ("WEBVTT\n\nNOTE a long note that is not a cue at all, and is far over the line limit\n\n"
                 "intro\n00:01.000 --> 00:03.000 align:center\n<v Ana><i>Short line</i>\n")
        self.assertEqual(subs.check(subs.parse(track)), [])

    def test_limits_can_be_set_for_children_s_content(self):
        cue = [{"start_ms": 0, "end_ms": 1000, "text": "eighteen chars !!!"}]
        self.assertEqual(codes(subs.check(cue)), [])
        self.assertEqual(codes(subs.check(cue, max_cps=17)), ["SUB105"])


class PostCheckTests(unittest.TestCase):
    def test_counts_match_the_platforms_published_examples(self):
        for platform, text, expected in [("x", "Hello, world! 👋", 16), ("x", "https://example.com/very/long/path", 23),
                                         ("x", "日本語", 6), ("threads", "👍🏽", 8), ("threads", "👨‍👩‍👧‍👦", 25),
                                         ("bluesky", "👨‍👩‍👧‍👦", 1), ("bluesky", "🇫🇷", 1),
                                         ("bluesky", "e\u0301", 1), ("instagram", "café", 4)]:
            with self.subTest(platform=platform, text=text):
                self.assertEqual(post.length(text, platform), expected)

    def test_limits_and_instagram_tag_caps(self):
        self.assertEqual(codes(post.check("a" * 281, "x")), ["CAP201"])
        self.assertEqual(codes(post.check("a" * 280, "x")), [])
        tags = " ".join(f"#t{i}" for i in range(6))
        self.assertEqual(codes(post.check(tags, "instagram")), ["CAP202"])
        self.assertEqual(codes(post.check(" ".join(f"#t{i}" for i in range(31)), "instagram")), ["CAP203"])
        self.assertEqual(codes(post.check(" ".join(f"@u{i}" for i in range(21)), "instagram")), ["CAP204"])

    def test_threads_report_the_post_and_line(self):
        found = post.check("First\n---\n\n---\n" + "x" * 501 + "\n---\n", "threads", thread=True)
        self.assertEqual([(f["code"], f["line"]) for f in found], [("THR301", 3), ("CAP201", 5)])

    def test_sponsored_posts_need_an_early_disclosure_outside_the_hashtags(self):
        check = lambda text, **kw: codes(post.check(text, "instagram", sponsored=True, **kw))
        self.assertEqual(check("Ad: Acme sent me this lamp.\n#lamp"), [])
        self.assertEqual(check("Iklan: Kedai Pak Ali belanja saya kopi."), [])
        self.assertEqual(check("广告｜这款台灯是品牌送的。"), [])
        self.assertEqual(check("Nice lamp."), ["DIS601"])
        self.assertEqual(check("Nice lamp.\n#lamp #desk #ad #setup"), ["DIS602", "DIS603"])
        self.assertEqual(check("Thanks to Acme for the free lamp.", disclosures=["Thanks to Acme for the free"]), [])
        self.assertEqual(codes(post.check("A thread.\n---\n#ad Acme paid for this", "x", thread=True,
                                          sponsored=True)), ["DIS602"])

    def test_a_word_containing_ad_is_not_a_disclosure(self):
        self.assertEqual(codes(post.check("I read a lot and had a headache.", "instagram", sponsored=True)),
                         ["DIS601"])

    def test_the_thread_skill_ships_the_same_checker(self):
        self.assertEqual((SKILLS / "social-captions/scripts/check_post.py").read_bytes(),
                         (SKILLS / "social-thread/scripts/check_post.py").read_bytes())


class AltCheckTests(unittest.TestCase):
    def test_each_rule(self):
        items = alt.load("Image of a potter at the wheel.\n\nIMG_2041.jpg\n\nA blue mug.\n\na blue mug.\n\n"
                         + "word " * 60)
        self.assertEqual([(f["code"], f["line"]) for f in alt.check(items)],
                         [("ALT402", 1), ("ALT405", 3), ("ALT406", 7), ("ALT404", 9)])
        self.assertEqual(codes(alt.check([{"alt": "x " * 600, "decorative": False, "label": "a", "line": 1}],
                                         "instagram")), ["ALT403"])

    def test_json_items_and_decorative_images(self):
        items = alt.load(json.dumps([{"id": "card 1", "alt": "", "decorative": True}, {"id": "card 2", "alt": ""}]))
        self.assertEqual([(f["code"], f["message"]) for f in alt.check(items)], [("ALT401", "card 2: no description")])

    def test_a_good_description_passes(self):
        self.assertEqual(alt.check(alt.load("Chart: bookings rose from 12 in March to 30 in May.")), [])


class LocalizationTests(unittest.TestCase):
    EN = "Repair Week: 6 March, 10:30am.\nRM2,500 for 3 sessions. Book at https://example.org/book or @kedai.pakali\n"

    def test_a_faithful_translation_is_clean(self):
        ms = "Minggu Baiki: 6 Mac, 10:30 pagi.\nRM2500 untuk 3 sesi. Tempah di https://example.org/book atau @kedai.pakali"
        zh = "维修周：3月6日上午10:30。\n３节课RM2,500。预约 https://example.org/book 或 @kedai.pakali"
        self.assertEqual(loc.compare(self.EN, ms), [])
        self.assertEqual(loc.compare(self.EN, zh), [])

    def test_changed_numbers_months_and_links(self):
        bad = "Minggu Baiki: 6 April, 10:30 pagi.\nRM2,050 untuk 3 sesi. https://example.org/booking @kedai.pakali"
        self.assertEqual(sorted(codes(loc.compare(self.EN, bad))), ["LOC501", "LOC502", "LOC503", "LOC504"])

    def test_may_the_verb_is_not_a_month(self):
        self.assertEqual(loc.compare("You may come in March.", "Boleh datang pada bulan Mac."), [])


class CreatorLintTests(unittest.TestCase):
    def lint(self, *args):
        return subprocess.run([sys.executable, str(LINT), *map(str, args)], capture_output=True, text=True)

    def test_every_rule_is_listed_once_with_a_source_or_reason(self):
        result = self.lint("--list-rules")
        self.assertEqual(result.returncode, 0, result.stderr)
        listed = [line.split()[0] for line in result.stdout.splitlines()]
        self.assertEqual(len(listed), len(set(listed)))
        self.assertGreaterEqual(len(listed), 29)
        for code in listed:
            with self.subTest(code=code):
                explained = self.lint("--explain", code.lower())
                self.assertEqual(explained.returncode, 0)
                self.assertGreater(len(explained.stdout), 60)

    def test_exit_codes_select_ignore_and_json(self):
        with tempfile.TemporaryDirectory() as td:
            caption = Path(td) / "caption.txt"
            caption.write_text("Nice lamp.\n#a #b #c #d #e #f\n", encoding="utf-8")
            failing = self.lint("post", caption, "--platform", "instagram", "--sponsored")
            self.assertEqual(failing.returncode, 1)
            self.assertIn("DIS601", failing.stdout)
            self.assertEqual(self.lint("post", caption, "--platform", "instagram", "--sponsored",
                                       "--ignore", "DIS").returncode, 0)
            self.assertEqual(self.lint("post", caption, "--platform", "instagram", "--strict").returncode, 1)
            found = json.loads(self.lint("post", caption, "--platform", "instagram", "--json",
                                         "--select", "CAP").stdout)
            self.assertEqual([f["code"] for f in found], ["CAP202"])
        self.assertEqual(self.lint("subtitles", ROOT / "examples/creator-captions/example.vtt").returncode, 0)
        self.assertEqual(self.lint("subtitles", "/no/such/file.srt").returncode, 2)
        self.assertEqual(self.lint("--explain", "NOPE1").returncode, 2)


if __name__ == "__main__":
    unittest.main()
