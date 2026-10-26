from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.common import common
from Src.Core.abstract_convert_factory import abstract_convert_factory

class reference_convertor(abstract_convertor):
    """
    Конвертер для формирования словаря по ссылочным типам
    Преобразует сущности base_model в словарное представление ссылки
    """

    def __init__(self, factory: abstract_convert_factory = None):
        super().__init__(factory)
        
    @staticmethod
    def _get_base_fields() -> list:
        """
        Динамическое извлечение свойств base_model через интроспекцию
        """
        return [
            attr for attr in dir(base_model)
            if not attr.startswith("_") and isinstance(getattr(base_model, attr, None), property)
        ]

    def _create_reference(self, item: base_model) -> dict:
        """
        Формирует словарь ссылки на основе свойств базовой модели
        """
        return {field: getattr(item, field, None) for field in self._get_base_fields()}

    def Convert(self, item: object, field_name: str = None) -> dict:
        """
        Преобразует ссылочную сущность (base_model) или извлекает ссылочные поля из объекта
        """
        if item is None:
            raise arguments_exception("item", "Значение не может быть None")

        # Защита от несовместимых примитивных типов
        if isinstance(item, (int, float, str, bool)):
            raise arguments_exception(
                "item",
                f"Ожидалась ссылочная сущность (base_model), получено: {type(item).__name__}"
            )

        # Если явно передано имя поля для одиночной ссылки
        if field_name is not None and isinstance(item, base_model):
            return {field_name: self._create_reference(item)}

        # Передан словарь — фильтруем ссылки
        if isinstance(item, dict):
            return {
                k: self._create_reference(v)
                for k, v in item.items()
                if isinstance(v, base_model)
            }

        # Извлекаем поля-ссылки из объекта через рефлексию
        try:
            fields = common.get_fields(item, is_common=True)
            result = {}
            for field in fields:
                val = getattr(item, field, None)
                if isinstance(val, base_model) and val is not item:
                    result[field] = self._create_reference(val)

            # Если объект содержит вложенные ссылки (nomenclature_model -> group, unit)
            if result:
                return result

            # Если вложенных ссылок нет, но сам объект == ссылка (base_model)
            if isinstance(item, base_model):
                return self._create_reference(item)

            return result
        except Exception:
            raise arguments_exception(
                "item",
                f"Неподдерживаемый тип данных для reference_convertor: {type(item).__name__}"
            )
