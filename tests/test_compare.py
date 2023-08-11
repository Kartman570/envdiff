import unittest
from envdiff.compare import compare
from envdiff.validate import validate


class CompareTests(unittest.TestCase):
    def test_changes(self):
        result = compare({"A": "secret-one", "B": "x"}, {"A": "secret-two", "C": "y"})
        self.assertEqual(result, [{"key": "A", "state": "changed"},
                                  {"key": "B", "state": "removed"},
                                  {"key": "C", "state": "added"}])
        self.assertNotIn("secret", str(result))

    def test_ignore_pattern(self):
        self.assertEqual(compare({"LOCAL_A": "1"}, {}, ["LOCAL_*"]), [])

    def test_validation(self):
        errors = validate({"PORT": "90000", "DEBUG": "perhaps"}, {
            "PORT": {"type": "integer", "max": 65535}, "TOKEN": {"required": True},
            "DEBUG": {"type": "boolean"}})
        self.assertEqual(len(errors), 3)

    def test_empty_is_missing(self):
        self.assertEqual(len(validate({"TOKEN": ""}, {"TOKEN": {"required": True}})), 1)
