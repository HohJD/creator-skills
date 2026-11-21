import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(rel,name):
 spec=importlib.util.spec_from_file_location(name,ROOT/rel)
 module=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(module)
 return module

class PackageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.validator=load('tools/validate_package.py','validator')
  cls.linter=load('tools/lint_package.py','linter')
  cls.installer=load('tools/install.py','installer')
  cls.valid=json.loads((ROOT/'fixtures/valid-package.json').read_text())
  cls.valid.pop('_expected_valid')
 def test_valid_package(self):self.assertEqual(self.validator.validate(self.valid),[])
 def test_invalid_claim(self):
  bad=json.loads((ROOT/'fixtures/bad-unverified.json').read_text());bad.pop('_expected_valid')
  self.assertTrue(any('unverified critical' in x for x in self.validator.validate(bad)))
 def test_unknown_claim_id(self):
  bad=json.loads((ROOT/'fixtures/bad-unknown-ref.json').read_text());bad.pop('_expected_valid')
  self.assertTrue(any('unknown claim ref' in x for x in self.validator.validate(bad)))
 def test_sponsored_cta_missing(self):
  bad=json.loads((ROOT/'fixtures/bad-cta.json').read_text());bad.pop('_expected_valid')
  self.assertTrue(any('CTA not present' in x for x in self.validator.validate(bad)))
 def test_lint(self):self.assertEqual(self.linter.lint(),[])
 def test_installs_both_hosts(self):
  with tempfile.TemporaryDirectory() as td:
   target=Path(td)
   for agent in ('claude','codex'):
    paths=self.installer.install(agent,'project',target)
    self.assertEqual(len(paths),1)
    self.assertTrue(all((p/'SKILL.md').is_file() for p in paths))
   with self.assertRaises(FileExistsError):self.installer.install('claude','project',target)

if __name__=='__main__':unittest.main()
