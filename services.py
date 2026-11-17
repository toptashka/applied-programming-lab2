import os
import re
import requests
import exceptions


# Определение типа пользовательского ввода: URL, файл или строка кода
def parsing_input(raw_input: str) -> str:
    if re.fullmatch(r'(?:http|https)://\S+', raw_input):
        return "url"
    elif os.path.isfile(raw_input):
        return "file"
    else:
        return "string"


# Получение исходного текста веб-страницы по URL-ссылке
def _process_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        raise exceptions.NetworkAccessError(f"Could not reach or fetch URL: {url}")


# Чтение текстового содержимого из локального файла
def _process_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (OSError, UnicodeDecodeError):
        raise exceptions.FileReadError(f"Permission denied or unable to read file: {file_path}")


# Поиск всех видов комментариев в тексте с помощью регулярного выражения
def _extract_comments(text: str) -> list[str]:
    # Шаблоны строковых литералов в кавычках (для игнорирования символов // и # внутри строк)
    double_quotes = r'"(?:\\.|[^"\\])*"'
    single_quotes = r"'(?:\\.|[^'\\])*'"

    # Шаблоны многострочных, HTML и однострочных комментариев
    multiline_comment = r'/\*[\s\S]*?\*/'
    html_comment = r'<!--[\s\S]*?-->'
    slash_comment = r'(?<![:/])//(?!/)[^\r\n<]*'
    hash_comment = r'#[^\r\n<]*'

    # Объединение шаблонов комментариев в захватывающую группу
    comments_group = (
        f"({multiline_comment}|{html_comment}|{slash_comment}|{hash_comment})"
    )

    full_pattern = f"{double_quotes}|{single_quotes}|{comments_group}"
    raw_matches = re.findall(full_pattern, text)

    # Фильтрация пустых строк, оставшихся после пропуска строковых литералов в кавычках
    comments = [match for match in raw_matches if match != ""]

    return comments


# Главная функция получения списка комментариев в зависимости от источника данных
def get_comments(raw_input: str) -> list[str]:
    input_type = parsing_input(raw_input)

    if input_type == "url":
        text = _process_url(raw_input)
    elif input_type == "file":
        text = _process_file(raw_input)
    else:
        text = raw_input

    return _extract_comments(text)