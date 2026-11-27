from enum import Enum


class filter_type(Enum):
    """
    Перечисление вариантов сравнения при фильтрации данных
    """
    EQUALS = "EQUALS"  # Полное совпадение
    LIKE = "LIKE"      # Вхождение подстроки (частичное совпадение)

    @classmethod
    def from_value(cls, value: object) -> "filter_type":
        """
        Преобразует переданное значение (Enum или строку) в filter_type
        Использует словарь соответствий 
        """
        if isinstance(value, cls):
            return value

        mapping = {
            "EQUALS": cls.EQUALS,
            "EQ": cls.EQUALS,
            "LIKE": cls.LIKE,
            "CONTAINS": cls.LIKE,
        }
        key = str(value).strip().upper() if value is not None else ""
        return mapping.get(key, cls.EQUALS)

    @staticmethod
    def match(source: str, query: str, mode: "filter_type") -> bool:
        """
        Проверка соответствия значения source запросу query в режиме mode
        Регистронезависимое сравнение с предварительной очисткой от пробелов
        """
        if query is None or len(str(query).strip()) == 0:
            return True

        src = str(source).strip().lower() if source is not None else ""
        tgt = str(query).strip().lower()

        m = filter_type.from_value(mode)
        if m == filter_type.LIKE:
            return tgt in src
        return src == tgt
