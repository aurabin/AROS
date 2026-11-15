import pathlib
import tempfile
import unittest

from check_manifest import validate

class ManifestTests(unittest.TestCase):
    def test_empty_manifest(self):
        self.assertEqual(validate({"components": []}, pathlib.Path(".")), [])

    def test_missing_metadata_rejected(self):
        self.assertTrue(validate({"components": [{"name": "example"}]}, pathlib.Path(".")))

    def test_approved_requires_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "NOTICE").write_text("copyright", encoding="utf-8")
            item = dict(name="x", source_url="https://example.org", revision="abc",
                        license_expression="MIT", copyright="Example",
                        notice_path="NOTICE", review_status="approved")
            self.assertTrue(validate({"components": [item]}, root))
            item["review_reference"] = "review-123"
            self.assertEqual(validate({"components": [item]}, root), [])

if __name__ == "__main__":
    unittest.main()
