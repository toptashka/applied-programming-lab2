import unittest
from services import (
    parsing_input,
    get_comments
)


# Тестирование маршрутизатора и определения типа входных данных
class TestParsingInput(unittest.TestCase):
    def test_recognizes_https_url(self) -> None:
        self.assertEqual(parsing_input("https://docs.python.org/3/"), "url")

    def test_recognizes_http_url(self) -> None:
        self.assertEqual(parsing_input("http://stankin.ru"), "url")

    def test_recognizes_existing_file(self) -> None:
        self.assertEqual(parsing_input("test.txt"), "file")

    def test_recognizes_plain_string(self) -> None:
        self.assertEqual(parsing_input('print("Hello World!") // comment'), "string")

    def test_rejects_url_without_protocol(self) -> None:
        self.assertEqual(parsing_input("stankin.ru"), "string")

    def test_rejects_unsupported_protocol_ftp(self) -> None:
        self.assertEqual(parsing_input("ftp://stankin.ru/files/doc.pdf"), "string")

    def test_rejects_empty_protocol(self) -> None:
        self.assertEqual(parsing_input("https://"), "string")

    def test_rejects_url_with_spaces(self) -> None:
        self.assertEqual(parsing_input("https://docs.python.org/3/ space"), "string")

    def test_rejects_code_containing_url(self) -> None:
        self.assertEqual(parsing_input('url = "https://docs.python.org/3/"'), "string")

    def test_rejects_non_existent_file(self) -> None:
        self.assertEqual(parsing_input("missing_file_999.py"), "string")

    def test_rejects_directory_as_file(self) -> None:
        self.assertEqual(parsing_input("."), "string")


# Тестирование регулярного выражения на строках кода и пограничных случаях
class TestExtractCommentsFromStrings(unittest.TestCase):
    def test_extracts_single_line_slash_comment(self) -> None:
        code = "int a = 5; // initialize variable"
        self.assertEqual(get_comments(code), ["// initialize variable"])

    def test_extracts_python_hash_comment(self) -> None:
        code = "x = 10 # set x"
        self.assertEqual(get_comments(code), ["# set x"])

    def test_extracts_multiline_comment(self) -> None:
        code = "/* line 1\nline 2 */ int b = 0;"
        self.assertEqual(get_comments(code), ["/* line 1\nline 2 */"])

    def test_extracts_html_comment(self) -> None:
        code = "<div><!-- hidden block --></div>"
        self.assertEqual(get_comments(code), ["<!-- hidden block -->"])

    def test_ignores_comments_inside_double_quotes(self) -> None:
        code = 'print("Fake // and # and /* comment */") // real comment'
        self.assertEqual(get_comments(code), ["// real comment"])

    def test_ignores_comments_inside_single_quotes(self) -> None:
        code = "text = 'Fake # comment // here' # real python comment"
        self.assertEqual(get_comments(code), ["# real python comment"])

    def test_ignores_urls_in_code(self) -> None:
        code = "Link: https://docs.python.org/3/ // actual comment"
        self.assertEqual(get_comments(code), ["// actual comment"])

    def test_ignores_triple_slashes(self) -> None:
        code = "/// triple slash or file:///C:/test.txt"
        self.assertEqual(get_comments(code), [])

    def test_lazy_matching_two_multiline_comments_on_same_line(self) -> None:
        code = "/* first */ int x = 1; /* second */"
        self.assertEqual(get_comments(code), ["/* first */", "/* second */"])

    def test_returns_empty_list_when_no_comments(self) -> None:
        code = "int main() { return 0; }"
        self.assertEqual(get_comments(code), [])


# Интеграционное тестирование извлечения комментариев из файла и по URL
class TestExtractCommentsFromFileAndUrl(unittest.TestCase):
    def test_extracts_exact_comments_from_file(self) -> None:
        expected = [
            "// first file comment",
            "/* second\nmultiline comment */",
            "# third python comment"
        ]
        self.assertEqual(get_comments("test.txt"), expected)

    def test_extracts_comments_from_python_docs_url(self) -> None:
        url = "https://docs.python.org/3/tutorial/introduction.html"
        result = get_comments(url)
        self.assertIn("# this is the first comment", result)
        self.assertIn("# and this is the second comment", result)
        self.assertIn("# ... and now a third!", result)


if __name__ == '__main__':
    unittest.main(verbosity=2)