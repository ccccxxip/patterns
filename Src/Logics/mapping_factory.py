"""
Фабрика маппинга (десериализации) DTO -> Domain Models
Реализует шаблон Фабрика, рекурсивную сборку графа объектов и защиту от дублирования через identity_cache
"""
import json
from Src.Core.exception import arguments_exception
from Src.Core.nomenclature_type import nomenclature_type
from Src.Models.warehouse_model import warehouse_model
from Src.Models.unit_model import unit_model
from Src.Models.nomenclature_group_model import nomenclature_group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.ingredient_model import ingredient_model
from Src.Models.recipe_model import recipe_model
from Src.Dtos.storage_dto import (
    warehouse_dto,
    unit_dto,
    nomenclature_group_dto,
    nomenclature_dto,
    ingredient_dto,
    recipe_dto,
    storage_dto
)
from Src.Logics.identity_cache import identity_cache


class mapping_factory:
    """
    Фабрика преобразования DTO в доменные модели
    """
    def __init__(self, cache: identity_cache = None):
        """
        Инициализация фабрики с возможностью передачи внешнего кэша
        """
        self._cache = cache if cache is not None else identity_cache()

        # Таблица соответствий 
        self.__type_mapping = {
            warehouse_dto: self.map_warehouse,
            unit_dto: self.map_unit,
            nomenclature_group_dto: self.map_group,
            nomenclature_dto: self.map_nomenclature,
            ingredient_dto: self.map_ingredient,
            recipe_dto: self.map_recipe,
            storage_dto: self.map_storage,
        }

    @property
    def cache(self) -> identity_cache:
        """Возвращает ссылку на кэш идентичности"""
        return self._cache

    @staticmethod
    def _parse_nomenclature_type(value: str) -> nomenclature_type:
        """
        Преобразует строковое значение типа из JSON в Enum nomenclature_type
        """
        for item in nomenclature_type:
            if item.value == value or item.name == value:
                return item
        return nomenclature_type.PRODUCT

    def map(self, dto_object: object) -> object:
        """
        Единый фабричный метод маппинга: определяет метод по типу входного DTO
        """
        if dto_object is None:
            return None

        dto_type = type(dto_object)
        mapper = self.__type_mapping.get(dto_type)

        if mapper is None:
            raise arguments_exception(
                "dto_object",
                f"Не найден маппер для типа DTO: {dto_type.__name__}"
            )

        return mapper(dto_object)

    def map_warehouse(self, dto: warehouse_dto) -> warehouse_model:
        """Маппинг склада"""
        if not dto:
            return None

        cached = self._cache.get(dto.id, "warehouse")
        if cached:
            return cached

        data = {"id": dto.id, "name": dto.name, "address": dto.address}
        item = warehouse_model.create(data)

        self._cache.add(item.id, item, "warehouse")
        return item

    def map_unit(self, dto: unit_dto) -> unit_model:
        """Маппинг единицы измерения"""
        if not dto:
            return None

        cached = self._cache.get(dto.id, "unit")
        if cached:
            return cached

        # Рекурсивный маппинг базовой единицы, если она задана
        base_unit_model = self.map_unit(dto.base_unit) if dto.base_unit else None

        data = {"id": dto.id, "name": dto.name, "ratio": dto.ratio}
        item = unit_model.create(data, base_unit=base_unit_model)

        self._cache.add(item.id, item, "unit")
        return item

    def map_group(self, dto: nomenclature_group_dto) -> nomenclature_group_model:
        """Маппинг группы номенклатуры"""
        if not dto:
            return None

        cached = self._cache.get(dto.id, "group")
        if cached:
            return cached

        data = {"id": dto.id, "name": dto.name}
        item = nomenclature_group_model.create(data)

        self._cache.add(item.id, item, "group")
        return item

    def map_nomenclature(self, dto: nomenclature_dto) -> nomenclature_model:
        """Маппинг номенклатуры"""
        if not dto:
            return None

        cached = self._cache.get(dto.id, "nomenclature")
        if cached:
            return cached

        group_model = self.map_group(dto.group)
        unit_model_obj = self.map_unit(dto.unit)
        nom_type = self._parse_nomenclature_type(dto.type)

        data = {"id": dto.id, "name": dto.name, "full_name": dto.full_name}
        item = nomenclature_model.create(data, group=group_model, unit=unit_model_obj, nom_type=nom_type)

        self._cache.add(item.id, item, "nomenclature")
        return item

    def map_ingredient(self, dto: ingredient_dto) -> ingredient_model:
        """Маппинг строки ингредиента"""
        if not dto:
            return None

        cached = self._cache.get(dto.id, "ingredient")
        if cached:
            return cached

        nom_model = self.map_nomenclature(dto.nomenclature)
        unit_model_obj = self.map_unit(dto.unit)
        sub_recipe_model = self.map_recipe(dto.recipe) if dto.recipe else None

        data = {"id": dto.id, "net_weight": dto.net_weight, "gross_weight": dto.gross_weight}
        item = ingredient_model.create(data, nomenclature=nom_model, unit=unit_model_obj, recipe=sub_recipe_model)

        self._cache.add(item.id, item, "ingredient")
        return item

    def map_recipe(self, dto: recipe_dto) -> recipe_model:
        """Маппинг технологической карты через фабричный метод модели"""
        if not dto:
            return None

        cached = self._cache.get(dto.id, "recipe")
        if cached:
            return cached

        owner_model = self.map_nomenclature(dto.owner)
        data = {
            "id": dto.id,
            "name": dto.name,
            "preparation_method": dto.preparation_method,
            "portions": dto.portions
        }
        item = recipe_model.create(data, owner=owner_model)

        # Регистрируем в кэше до обхода ингредиентов
        self._cache.add(item.id, item, "recipe")

        # Рекурсивное наполнение ингредиентами
        for ing_dto in dto.ingredients:
            ing_model = self.map_ingredient(ing_dto)
            if ing_model:
                item.add_ingredient(ing_model)

        return item

    def map_storage(self, dto: storage_dto) -> dict:
        """
        Маппинг корневого хранилища
        """
        if not dto:
            return {}

        warehouses = [self.map_warehouse(w) for w in dto.warehouse if w]
        units = [self.map_unit(u) for u in dto.unit if u]
        groups = [self.map_group(g) for g in dto.group if g]
        nomenclatures = [self.map_nomenclature(n) for n in dto.nomenclature if n]
        recipes = [self.map_recipe(r) for r in dto.recipe if r]

        return {
            "warehouse": warehouses,
            "unit": units,
            "group": groups,
            "nomenclature": nomenclatures,
            "recipe": recipes
        }

    def from_json(self, json_text: str) -> dict:
        """
        Десериализация JSON строки в структуру доменных моделей
        """
        if not json_text or not json_text.strip():
            raise arguments_exception("json_text", "JSON строка не может быть пустой")

        data = json.loads(json_text)
        dto = storage_dto.from_dict(data)
        return self.map_storage(dto)
