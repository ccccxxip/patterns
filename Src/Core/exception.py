class arguments_exception(Exception):
    """ Внутреннее исключение для сообщения об ошибках валидации аргументов моделей """

    __stack_trace: str = ""
    __message: str = ""
    __field: str = ""

    def __init__(self, field: str, message: str, stack_trace: str = ""):

        """
        Инициализирует исключение с указанием некорректного поля и сообщения об ошибке

        field: Имя поля, вызвавшего ошибку
        message: Описание ошибки
        stack_trace: Необязательная доп. информация 
        """

        self.__field = field.strip() if isinstance(field, str) else str(field)
        self.__message = message.strip() if isinstance(message, str) else str(message)
        self.__stack_trace = stack_trace.strip() if isinstance(stack_trace, str) else str(stack_trace)

    def __str__(self) -> str:

        """ Возвращает текстовое представление ошибки с указанием поля и сообщения """

        return f"Ошибка. Некорректный аргумент {self.__field}\n{self.__message}\n{self.__stack_trace}"