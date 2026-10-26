from datetime import datetime, date
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.exception import arguments_exception
from Src.Core.common import common
from Src.Core.abstract_convert_factory import abstract_convert_factory


class datetime_convertor(abstract_convertor):
    """
    Конвертер для формирования словаря по типу DateTime (datetime, date)
    Преобразует даты в строковое представление по стандарту ISO 8601
    """

    # Кортеж поддерживаемых типов даты и времени
    __datetime_types: tuple = (datetime, date)

    def __init__(self, factory: abstract_convert_factory = None):
        """
        Инициализация конвертера даты и времени
        """
        super().__init__(factory)

    def Convert(self, item: object, field_name: str = None) -> dict:
        """
        Преобразует значение DateTime или извлекает поля DateTime из объекта в словарь

        item: object
            Объект datetime, date или объект, содержащий поля даты

        field_name: str, optional
            Имя ключа в словаре для одиночного значения даты (по дефолтц "value")

        returns: dict
            Словарь вида {имя_поля: iso_строка_даты}

        """
        if item is None:
            raise arguments_exception("item", "Значение не может быть None")

        # Одиночный объект datetime или date
        if isinstance(item, self.__datetime_types):
            key = field_name if field_name is not None else "value"
            return {key: item.isoformat()}

        # Несовместимые типы
        if isinstance(item, (int, float, str, bool)):
            raise arguments_exception(
                "item",
                f"Ожидался тип DateTime (datetime/date), получено: {type(item).__name__}"
            )

        # Передан словарь — извлекаем только поля с датами
        if isinstance(item, dict):
            res = {
                k: v.isoformat() for k, v in item.items()
                if isinstance(v, self.__datetime_types)
            }
            if not res and item:
                raise arguments_exception(
                    "item",
                    "В переданном словаре отсутствуют поля типа DateTime"
                )
            return res

        # Передана доменная модель или объект со свойствами
        try:
            fields = common.get_fields(item, is_common=True)
            result = {}
            for field in fields:
                val = getattr(item, field, None)
                if isinstance(val, self.__datetime_types):
                    result[field] = val.isoformat()
            return result
        except Exception:
            raise arguments_exception(
                "item",
                f"Неподдерживаемый тип данных для datetime_convertor: {type(item).__name__}"
            )
