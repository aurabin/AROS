"""AROS One staging safety tests; run with python -m unittest discover."""
import copy
import json
import pathlib
import unittest
from validate import validate

BASE = pathlib.Path(__file__).with_name("distribution.json")

class AROSOneMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(BASE.read_text(encoding="utf-8"))

    def test_current_manifest(self):
        self.assertEqual(validate(self.data), [])

    def test_unreviewed_edition_cannot_be_enabled(self):
        data = copy.deepcopy(self.data)
        data["editions"][0]["enabled"] = True
        self.assertTrue(validate(data))

    def test_redistribution_must_be_disabled(self):
        data = copy.deepcopy(self.data)
        data["redistribution_authorized"] = True
        self.assertTrue(validate(data))

    def test_no_unreviewed_components(self):
        data = copy.deepcopy(self.data)
        data["components"] = [{"name": "unreviewed"}]
        self.assertTrue(validate(data))

    def test_both_abis_required(self):
        data = copy.deepcopy(self.data)
        data["editions"].pop()
        self.assertTrue(validate(data))

    def test_staging_status_required(self):
        data = copy.deepcopy(self.data)
        data["integration_status"] = "released"
        self.assertTrue(validate(data))

if __name__ == "__main__":
    unittest.main()
