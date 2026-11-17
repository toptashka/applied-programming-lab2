import re
import os

def parsing_input(raw_input: str) -> str:
    if re.fullmatch(r'(?:http|https)://\S+', raw_input):
        return "url"
    elif os.path.isfile(raw_input):
        return "file"
    else:
        return "string"


# функция на работу с URL ссылками (строка с ввода)

# пока не знаю как это работает


# функция на работу с файлами (строка с ввода)

# открыаем файл через цикл (построчно)
# если строка попадает по регулярку: добавлем в массив


# функция на работу с обычными строками (строка с ввода)

# если строка попадает по регулярку: добавлем в массив