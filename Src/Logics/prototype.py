from typing import List, Any
from Src.Core.abstract_prototype import abstract_prototype
from Src.Dtos.filter_dto import filter_dto
from Src.Core.filter_type import filter_type
from Src.Core.common import common
from Src.Core.base_model import base_model


class prototype(abstract_prototype):
    """
    Шаблон проектирования «Прототип»
    Хранит набор доменных сущностей и порождает новые экземпляры прототипа
    через метод clone(filter_dto) с применением фильтрации
    Поддерживает каскадную фильтрацию: prototype(data).clone(f1).clone(f2)
    """

    def __init__(self, data: List[Any] = None):
        """
        Инициализация прототипа коллекцией данных
        """
        self.__data: List[Any] = list(data) if data is not None else []

    @property
    def data(self) -> List[Any]:
        """Текущий набор данных прототипа"""
        return self.__data

    def clone(self, filter_: filter_dto = None) -> "prototype":
        """
        Создает новый экземпляр прототипа (клон)
        Если передан filter_dto, отфильтровывает данные по критериям
        """
        if filter_ is None or filter_.is_empty:
            return prototype(list(self.__data))

        filtered_data = [item for item in self.__data if self._matches(item, filter_)]
        return prototype(filtered_data)

    @classmethod
    def _matches(cls, item: Any, filter_: filter_dto) -> bool:
        """
        Проверяет соответствие объекта фильтру через рефлексию
        """
        return cls._check_entity(item, filter_, visited=set())

    @classmethod
    def _matches_current(cls, obj: Any, filter_: filter_dto) -> bool:
        """
        Проверяет совпадение критериев фильтра на объекте через рефлексию
        """
        conditions = []
        obj_fields = set(common.get_fields(obj))

        # Свойства filter_dto
        for field in common.get_fields(filter_):
            if field in ("filter_type", "is_empty", "filters", "start_period", "end_period"):
                continue
            val = getattr(filter_, field, None)
            if val and field in obj_fields:
                conditions.append(filter_type.match(getattr(obj, field, None), val, filter_.filter_type))

        # Критерии из списка filter_item_dto
        for item in filter_.filters:
            if item.field_name in obj_fields:
                conditions.append(filter_type.match(getattr(obj, item.field_name, None), item.value, item.filter_type))

        # Фильтрация периода (если у объекта есть свойство period)
        if "period" in obj_fields:
            period = getattr(obj, "period", None)
            if filter_.start_period is not None:
                conditions.append(period is not None and period >= filter_.start_period)
            if filter_.end_period is not None:
                conditions.append(period is not None and period <= filter_.end_period)

        return all(conditions) if conditions else False

    @classmethod
    def _get_children(cls, obj: Any):
        """генератор всех дочерних доменных сущностей"""
        for field in common.get_fields(obj):
            val = getattr(obj, field, None)
            if isinstance(val, base_model):
                yield val
            elif isinstance(val, list):
                yield from (x for x in val if isinstance(x, base_model))

    @classmethod
    def _check_entity(cls, obj: Any, filter_: filter_dto, visited: set) -> bool:
        """Универсальная проверка графа сущностей"""
        if not isinstance(obj, base_model) or id(obj) in visited:
            return False
        visited.add(id(obj))

        if cls._matches_current(obj, filter_):
            return True

        return any(cls._check_entity(child, filter_, visited) for child in cls._get_children(obj))