import unittest
from envdiff.parser import parse


class ParserTests(unittest.TestCase):
    def test_quotes_and_comments(self):
        values = parse("export NAME='hello # world'\nX=one # comment\nEMPTY=\n")
        self.assertEqual(values, {"NAME": "hello # world", "X": "one", "EMPTY": ""})

    def test_escape(self):
        self.assertEqual(parse('X="first\\nsecond"')['X'], "first\nsecond")

    def test_duplicate(self):
        with self.assertRaisesRegex(ValueError, "Duplicate key X"):
            parse("X=one\nX=two")

    def test_errors_hide_values(self):
        for content in ('TOKEN="super-secret', 'bad-key=super-secret', 'super-secret'):
            with self.assertRaises(ValueError) as caught:
                parse(content)
            self.assertNotIn("super-secret", str(caught.exception))
