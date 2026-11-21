from typing import List
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


class filter_dto:
    """
    DTO модель для передачи параметров фильтрации данных
    Поддерживает фильтрацию по name, id
    с выбором алгоритма сравнения (EQUALS или LIKE)
    Также поддерживает список критериев filters (список filter_item_dto)
    """

    def __init__(self):
        self.__name: str = ""
        self.__id: str = ""
        self.__filter_type: filter_type = filter_type.EQUALS
        self.__filters: List[filter_item_dto] = []

    @property
    def name(self) -> str:
        """Наименование сущности для фильтрации"""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = str(value).strip() if value is not None else ""

    @property
    def id(self) -> str:
        """Уникальный код сущности для фильтрации"""
        return self.__id

    @id.setter
    def id(self, value: str):
        self.__id = str(value).strip() if value is not None else ""

    @property
    def filter_type(self) -> filter_type:
        """Режим фильтрации (EQUALS / LIKE)"""
        return self.__filter_type

    @filter_type.setter
    def filter_type(self, value):
        self.__filter_type = filter_type.from_value(value)

    @property
    def filters(self) -> List[filter_item_dto]:
        """Список отдельных условий фильтрации"""
        return self.__filters

    @filters.setter
    def filters(self, value: List[filter_item_dto]):
        raw = value if isinstance(value, list) else []
        self.__filters = [filter_item_dto.from_dict(x) if isinstance(x, dict) else x for x in raw]

    @property
    def is_empty(self) -> bool:
        """Флаг отсутствия критериев фильтрации"""
        return len(self.__name) == 0 and len(self.__id) == 0 and len(self.__filters) == 0

    @is_empty.setter
    def is_empty(self, value):
        """Сеттер-заглушка для совместимости с рефлексией"""
        pass

    @classmethod
    def from_dict(cls, data: dict) -> "filter_dto":
        """
        Фабричный метод создания DTO из словаря с использованием рефлексии
        """
        if not isinstance(data, dict):
            return None

        dto = cls()
        fields = common.get_fields(dto)

        for field in fields:
            if field in data and data[field] is not None:
                setattr(dto, field, data[field])

        return dto
