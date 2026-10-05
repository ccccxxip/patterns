from Src.Core.exception import arguments_exception

class operation_exception(Exception):
    """Исключение при выполнении бизнес-операций"""
    pass

class validator:
    @staticmethod
    def validate(value, type_, len_=None, field_name: str = "argument") -> bool:
        """
        Валидация аргумента по типу и длине
        При ошибке генерирует arguments_exception
        """
        if value is None:
            raise arguments_exception(field_name, "Пустой аргумент")

        if not isinstance(value, type_):
            raise arguments_exception(
                field_name, 
                f"Некорректный тип. Ожидается {type_.__name__}, получен {type(value).__name__}"
            )

        if type_ is str:
            if len(str(value).strip()) == 0:
                raise arguments_exception(field_name, "Пустая строка")

            if len_ is not None and len(str(value).strip()) > len_:
                raise arguments_exception(field_name, f"Превышена максимальная длина ({len_})")

        return True