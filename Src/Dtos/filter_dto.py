from datetime import datetime
from typing import List, Optional
from Src.Core.common import common
from Src.Core.filter_type import filter_type
from Src.Dtos.filter_item_dto import filter_item_dto


class filter_dto:
    """
    DTO модель для передачи параметров фильтрации данных
    Поддерживает фильтрацию по name, id, периоду (start_period, end_period)
    с выбором алгоритма сравнения (EQUALS или LIKE)
    Также поддерживает список критериев filters (список filter_item_dto)
    """

    def __init__(self):
        self.__name: str = ""
        self.__id: str = ""
        self.__filter_type: filter_type = filter_type.EQUALS
        self.__filters: List[filter_item_dto] = []
        self.__start_period: Optional[datetime] = None
        self.__end_period: Optional[datetime] = None

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

    @staticmethod
    def _parse_period(value) -> Optional[datetime]:
        """Преобразование переданного значения в объект datetime"""
        if isinstance(value, datetime):
            return value
        if isinstance(value, str) and value.strip():
            return datetime.fromisoformat(value.strip())
        return None

    @property
    def start_period(self) -> Optional[datetime]:
        """Начало периода фильтрации"""
        return self.__start_period

    @start_period.setter
    def start_period(self, value):
        self.__start_period = self._parse_period(value)

    @property
    def end_period(self) -> Optional[datetime]:
        """Конец периода фильтрации"""
        return self.__end_period

    @end_period.setter
    def end_period(self, value):
        self.__end_period = self._parse_period(value)

    @property
    def is_empty(self) -> bool:
        """Флаг отсутствия критериев фильтрации"""
        return (
            len(self.__name) == 0
            and len(self.__id) == 0
            and len(self.__filters) == 0
            and self.__start_period is None
            and self.__end_period is None
        )

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
