# Базовый класс исключений для слоя бизнес-логики
class BusinessLogicError(Exception):
    pass


# Исключение при ошибках сетевого доступа к URL-ссылке
class NetworkAccessError(BusinessLogicError):
    pass


# Исключение при ошибках доступа или чтения локального файла
class FileReadError(BusinessLogicError):
    pass