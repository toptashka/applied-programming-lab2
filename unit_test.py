import unittest
from services import (
    parsing_input
)


class TestParsingInput(unittest.TestCase):
    def test_recognizes_url(self):
        test_string = "https://google.com"
        result = parsing_input(test_string)
        self.assertEqual(result, "url")

    def test_recognizes_file(self):
        test_string = "test.txt"
        result = parsing_input(test_string)
        self.assertEqual(result, "file")

    def test_recognizes_string(self):
        test_string = "print(\"Hello World!\") // comment"
        result = parsing_input(test_string)
        self.assertEqual(result, "string")


if __name__ == '__main__':
    unittest.main()