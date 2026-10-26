from datetime import datetime, date
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.common import common
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor
from enum import Enum
import json
from Src.Core.abstract_convert_factory import abstract_convert_factory


class convert_factory(abstract_convert_factory):
    """
    Класс-фабрика конвертеров данных
    Реализует abstract_convert_factory, подбирает конвертер по типу данных (метод create)
    и преобразует любые объекты в структуру словарей (метод Convert)
    """

    def __init__(self):
        """Инициализирует фабрику экземплярами спец конвертеров, связывая их с фабрикой"""
        self.__basic = basic_convertor(self)
        self.__datetime = datetime_convertor(self)
        self.__reference = reference_convertor(self)

        # Таблица соответствия типов для фабричного метода create
        self.__type_mapping: dict = {
            "basic": self.__basic,
            "datetime": self.__datetime,
            "reference": self.__reference,
            int: self.__basic,
            float: self.__basic,
            str: self.__basic,
            bool: self.__basic,
            datetime: self.__datetime,
            date: self.__datetime,
        }

    def to_json(self, item: object, indent: int = 4) -> str:
        """
        Сериализует объект любого типа в строку формата JSON
        """
        converted = self.Convert(item)
        return json.dumps(converted, ensure_ascii=False, indent=indent)

    def create(self, source_or_type: object) -> abstract_convertor:
        """
        Фабричный метод: подбирает конвертер по типу, объекту или строковому ключу
        """
        if source_or_type is None:
            raise arguments_exception("source_or_type", "Тип или объект не может быть None")

        # Поиск по строковому ключу ("basic", "datetime", "reference")
        if isinstance(source_or_type, str) and source_or_type.lower() in self.__type_mapping:
            return self.__type_mapping[source_or_type.lower()]

        target_type = source_or_type if isinstance(source_or_type, type) else type(source_or_type)

        # Прямой поиск в таблице (числа, строки, даты)
        if target_type in self.__type_mapping:
            return self.__type_mapping[target_type]

        # Доменные сущности (наследники base_model)
        if issubclass(target_type, base_model):
            return self.__reference

        raise arguments_exception(
            "source_or_type",
            f"Не удалось подобрать конвертер для типа: {target_type.__name__}"
        )

    def Convert(self, item: object, visited: set = None):
        """
        Преобразует объект любого типа в структуру словарей
        """
        if item is None:
            return None

        # Простые скалярные типы и даты подбираются через словарь фабрики
        item_type = type(item)
        if item_type in self.__type_mapping:
            return self.__type_mapping[item_type].Convert(item)["value"]


        if isinstance(item, Enum):
            return item.value

        if visited is None:
            visited = set()

        # Коллекции (списки, кортежи, множества)
        if isinstance(item, (list, tuple, set)):
            return [self.Convert(elem, visited) for elem in item]

        # Словари
        if isinstance(item, dict):
            return {k: self.Convert(v, visited) for k, v in item.items()}

        # Доменные сущности (наследники base_model)
        if isinstance(item, base_model):
            item_id = id(item)
            if item_id in visited:
                # Циклическая зависимость: возвращаем ссылочное представление
                return self.__reference.Convert(item)

            current_visited = set(visited)
            current_visited.add(item_id)

            result = {}
            # Базовые скалярные поля и даты
            result.update(self.__basic.Convert(item))
            result.update(self.__datetime.Convert(item))

            # Обрабатываем все свойства модели через рефлексию
            for field in common.get_fields(item, is_common=False):
                if field not in result:
                    val = getattr(item, field, None)
                    # Универсальная проверка ссылки объекта на самого себя
                    if val is item:
                        result[field] = None
                    else:
                        result[field] = self.Convert(val, current_visited)

            return result

        # Другой объект со свойствами
        try:
            return {field: self.Convert(getattr(item, field, None), visited)
                    for field in common.get_fields(item, is_common=False)}
        except Exception:
            return str(item)
