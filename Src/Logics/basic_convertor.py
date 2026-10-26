from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.exception import arguments_exception
from Src.Core.common import common


class basic_convertor(abstract_convertor):
    """
    Конвертер для формирования словаря по простым типам данных
    Поддерживает: int, float, str, bool
    """

    # Кортеж поддерживаемых типов
    __basic_types: tuple = (int, float, str, bool)

    def __init__(self, factory=None):
        """
        Инициализация базового конвертера
        """
        super().__init__(factory)

    def Convert(self, item: object, field_name: str = None) -> dict:
        """
        Преобразует простое значение или извлекает простые поля из объекта в словарь

        item: object
            Скалярное значение (int, float, str, bool) или объект со свойствами

        field_name: str, optional
            Имя ключа в словаре для одиночного скалярного значения (по дефолту "value")

        returns: dict
            Словарь вида {имя_поля: значение}
        """
        if item is None:
            raise arguments_exception("item", "Значение не может быть None")

        # Одиночное скалярное значение
        if isinstance(item, self.__basic_types):
            key = field_name if field_name is not None else "value"
            return {key: item}

        # Передан словарь — фильтруем только простые значения
        if isinstance(item, dict):
            return {
                k: v for k, v in item.items()
                if isinstance(v, self.__basic_types)
            }

        # Передана доменная модель или объект со свойствами
        try:
            fields = common.get_fields(item, is_common=True)
            result = {}
            for field in fields:
                val = getattr(item, field, None)
                if isinstance(val, self.__basic_types):
                    result[field] = val
            return result
        except Exception:
            raise arguments_exception(
                "item",
                f"Неподдерживаемый тип данных для basic_convertor: {type(item).__name__}"
            )
