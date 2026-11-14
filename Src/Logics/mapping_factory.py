"""
Фабрика маппинга (десериализации) DTO -> Domain Models
Реализует abstract_mapping_factory, динамическую рефлексию и защиту от дублирования через identity_cache
"""
import json
from typing import Dict, Type
from Src.Core.exception import arguments_exception
from Src.Core.nomenclature_type import nomenclature_type
from Src.Core.abstract_mapping_factory import abstract_mapping_factory
from Src.Models.warehouse_model import warehouse_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Dtos.warehouse_dto import warehouse_dto
from Src.Dtos.unit_dto import unit_dto
from Src.Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.ingredient_dto import ingredient_dto
from Src.Dtos.recipe_dto import recipe_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Logics.identity_cache import identity_cache


class mapping_factory(abstract_mapping_factory):
    """
    Фабрика динамического преобразования DTO в доменные модели
    таблица соответствия DTO <-> Domain + рефлексия
    """

    def __init__(self, cache: identity_cache = None):
        super().__init__()
        self._cache = cache if cache is not None else identity_cache()

        # Таблица соответствия
        self.__mapping: Dict[Type, Type] = {
            warehouse_dto:          warehouse_model,
            unit_dto:               unit_model,
            nomenclature_group_dto: nomenclature_group_model,
            nomenclature_dto:       nomenclature_model,
            ingredient_dto:         ingredient_model,
            recipe_dto:             recipe_model,
        }

    @property
    def cache(self) -> identity_cache:
        """Возвращает ссылку на кэш идентичности"""
        return self._cache

    @staticmethod
    def _parse_nomenclature_type(value: str) -> nomenclature_type:
        """Преобразует строковое значение типа из JSON в Enum nomenclature_type"""
        for item in nomenclature_type:
            if item.value == value or item.name == value:
                return item
        return nomenclature_type.PRODUCT

    def to_model(self, source: object) -> object:
        """
        Универсальный метод преобразования DTO в доменную модель
        Определяет тип DTO по таблице __mapping и создаёт модель через рефлексию
        """
        if source is None:
            return None

        if isinstance(source, storage_dto):
            return self._map_storage(source)

        source_type = type(source)
        domain_cls = self.__mapping.get(source_type)
        if domain_cls is None:
            raise arguments_exception(
                "source",
                f"Не найден маппер для типа DTO: {source_type.__name__}"
            )

        # Проверяем кэш идентичности по ID
        source_id = getattr(source, "id", None)
        if source_id:
            cached = self._cache.get(source_id, domain_cls.__name__)
            if cached is not None:
                return cached

        # Динамически извлекаем поля DTO через рефлексию
        data = {}
        for field, value in vars(source).items():
            if field.startswith("_"):
                continue
            if type(value) in self.__mapping:
                data[field] = self.to_model(value)
            elif isinstance(value, list):
                data[field] = [
                    self.to_model(item) if type(item) in self.__mapping else item
                    for item in value
                ]
            elif field == "type":
                nom_type = self._parse_nomenclature_type(value) if isinstance(value, str) else value
                data["type"] = nom_type
                data["nom_type"] = nom_type
            else:
                data[field] = value

        item = domain_cls.create(data)

        if source_id:
            self._cache.add(source_id, item, domain_cls.__name__)

        return item

    def to_dto(self, source: object) -> object:
        """Сконвертировать доменную модель в DTO"""
        if source is None:
            return None
        return source

    def map(self, dto_object: object) -> object:
        """Универсальная точка входа маппинга"""
        return self.to_model(dto_object)

    def _map_storage(self, dto: storage_dto) -> dict:
        """Преобразует корневой DTO хранилища в словарь списков доменных моделей"""
        if not dto:
            return {}
        return {
            "warehouse":   [self.to_model(w) for w in dto.warehouse    if w],
            "unit":        [self.to_model(u) for u in dto.unit         if u],
            "group":       [self.to_model(g) for g in dto.group        if g],
            "nomenclature":[self.to_model(n) for n in dto.nomenclature if n],
            "recipe":      [self.to_model(r) for r in dto.recipe       if r],
        }

    def from_json(self, json_text: str) -> dict:
        """Основной метод десериализации JSON в доменные модели"""
        if not json_text or not isinstance(json_text, str) or not json_text.strip():
            raise arguments_exception("json_text", "Строка JSON не может быть пустой")
        try:
            raw_data = json.loads(json_text)
        except Exception as e:
            raise arguments_exception("json_text", f"Некорректный формат JSON: {e}")
        dto = storage_dto.from_dict(raw_data)
        return self._map_storage(dto)