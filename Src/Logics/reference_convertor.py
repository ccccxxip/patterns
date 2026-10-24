from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.common import common


class reference_convertor(abstract_convertor):
    """
    Конвертер для формирования словаря по ссылочным типам
    Преобразует сущности base_model в словарное представление ссылки {"id": ..., "name": ...}
    """

    def Convert(self, item: object, field_name: str = None) -> dict:
        """
        Преобразует ссылочную сущность (base_model) или извлекает ссылочные поля из объекта

        item: object
            Сущность base_model или объект, содержащий свойства-ссылки на base_model

        field_name: str, optional
            Имя поля для обертки результата в {field_name: {"id": ..., "name": ...}}

        returns: dict
            Словарь вида {"id": ..., "name": ...} или {имя_поля_ссылки: {"id": ..., "name": ...}}
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
            return {field_name: {"id": item.id, "name": item.name}}

        # Передан словарь — фильтруем ссылки
        if isinstance(item, dict):
            return {
                k: {"id": v.id, "name": v.name}
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
                    result[field] = {"id": val.id, "name": val.name}

            # Если объект содержит вложенные ссылки (nomenclature_model -> group, unit)
            if result:
                return result

            # Если вложенных ссылок нет, но сам объект == ссылка (base_model)
            if isinstance(item, base_model):
                return {"id": item.id, "name": item.name}

            return result
        except Exception:
            raise arguments_exception(
                "item",
                f"Неподдерживаемый тип данных для reference_convertor: {type(item).__name__}"
            )
