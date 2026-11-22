from Src.Core.common import common
from Src.Core.filter_type import filter_type


class filter_item_dto:
    """
    Элемент критерия фильтрации отдельного поля
    """

    def __init__(self):
        self.__field_name: str = ""
        self.__value: str = ""
        self.__filter_type: filter_type = filter_type.EQUALS

    @property
    def field_name(self) -> str:
        """Имя поля для фильтрации"""
        return self.__field_name

    @field_name.setter
    def field_name(self, value: str):
        self.__field_name = str(value).strip() if value is not None else ""

    @property
    def value(self) -> str:
        """Значение поля для поиска"""
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = str(value).strip() if value is not None else ""

    @property
    def filter_type(self) -> filter_type:
        """Режим фильтрации (EQUALS / LIKE)"""
        return self.__filter_type

    @filter_type.setter
    def filter_type(self, value):
        self.__filter_type = filter_type.from_value(value)

    @classmethod
    def from_dict(cls, data: dict) -> "filter_item_dto":
        """Фабричный метод создания элемента фильтра из словаря с использованием рефлексии"""
        if not isinstance(data, dict):
            return None

        item = cls()
        fields = common.get_fields(item)
        for field in fields:
            if field in data and data[field] is not None:
                setattr(item, field, data[field])

        return item
