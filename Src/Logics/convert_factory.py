from datetime import datetime, date
import json
from Src.Core.abstract_convertor import abstract_convertor
from Src.Core.base_model import base_model
from Src.Core.exception import arguments_exception
from Src.Core.common import common
from Src.Logics.basic_convertor import basic_convertor
from Src.Logics.datetime_convertor import datetime_convertor
from Src.Logics.reference_convertor import reference_convertor


class convert_factory:
    """
    Класс-фабрика конвертеров данных
    Подбирает конвертер по типу данных (метод create) и преобразует
    любые объекты в структуру словарей (метод Convert)
    """

    def __init__(self):
        """Инициализирует фабрику экземплярами спец конвертеров"""
        self.__basic = basic_convertor()
        self.__datetime = datetime_convertor()
        self.__reference = reference_convertor()

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


    def Convert(self, item: object):
        """
        Преобразует объект любого типа в структуру словарей
        """
        if item is None:
            return None

        # Простые типы и даты
        if isinstance(item, (int, float, str, bool)):
            return self.__basic.Convert(item)["value"]

        if isinstance(item, (datetime, date)):
            return self.__datetime.Convert(item)["value"]

        # Коллекции (списки, кортежи, словари)
        if isinstance(item, (list, tuple, set)):
            return [self.Convert(elem) for elem in item]

        if isinstance(item, dict):
            return {k: self.Convert(v) for k, v in item.items()}

        # Доменные сущности
        if isinstance(item, base_model):
            result = {}
            result.update(self.__basic.Convert(item))
            result.update(self.__datetime.Convert(item))
            result.update(self.__reference.Convert(item))

            # Вложенные коллекции (список ингредиентов в рецепте)
            for field in common.get_fields(item, is_common=False):
                if field not in result:
                    val = getattr(item, field, None)
                    if isinstance(val, (list, tuple, set, dict)):
                        result[field] = self.Convert(val)

            return result

        # Другой объект со свойствами
        try:
            return {field: self.Convert(getattr(item, field, None))
                    for field in common.get_fields(item, is_common=False)}
        except Exception:
            return str(item)
