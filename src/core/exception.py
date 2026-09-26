class arguments_exception(Exception):
    __stack_trace: str = ""
    __message: str = ""
    __field: str = ""

    def __init__(self, field: str, message: str, stack_trace: str = ""):
        self.__field = field.strip() if isinstance(field, str) else str(field)
        self.__message = message.strip() if isinstance(message, str) else str(message)
        self.__stack_trace = stack_trace.strip() if isinstance(stack_trace, str) else str(stack_trace)

    def __str__(self) -> str:
        return f"Ошибка. Некорректный аргумент! {self.__field}\n{self.__message}\n{self.__stack_trace}"