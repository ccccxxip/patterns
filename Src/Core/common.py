from Src.Core.exception import arguments_exception


class common:
    """Набор общих статических методов рефлексии"""

    # Таблица правил: сопоставление ключевых слов из docstring свойства с заголовком
    __title_rules = (
        ("уникальный идентификатор", "Код"),
        ("полное наименование", "Полное наименование"),
        ("коэффициент", "Коэффициент"),
        ("базов", "Базовая единица"),
        ("единиц", "Единица измерения"),
        ("групп", "Группа"),
        ("тип", "Тип"),
        ("владел", "Блюдо"),
        ("общий вес брутто", "Итого Брутто"),
        ("вес брутто", "Брутто (г)"),
        ("общий вес нетто", "Итого Нетто"),
        ("вес нетто", "Нетто (г)"),
        ("порций", "Порций"),
        ("способ приготовления", "Способ приготовления"),
        ("рецепт", "Рецепт"),
        ("номенклатур", "Номенклатура"),
        ("состав", "Состав"),
        ("ингредиент", "Состав"),
        ("наименование", "Наименование"),
    )

    @staticmethod
    def get_fields(source, is_common: bool = False) -> list:
        """
        Получить полный список полей (@property) любой модели через рефлексию:
            - is_common = True: исключить из списка словари и списки (только скалярные поля и связи)
        """
        if source is None:
            raise arguments_exception("source", "Некорректно переданы аргументы!")

        items = list(filter(lambda x: not x.startswith("_"), dir(source)))
        result = []

        for item in items:
            attribute = getattr(source.__class__, item, None)
            if isinstance(attribute, property):
                value = getattr(source, item)

                # Флаг: только простые типы и одиночные модели (исключаем списки и словари)
                if is_common is True and (isinstance(value, dict) or isinstance(value, list)):
                    continue

                result.append(item)

        return result

    @staticmethod
    def get_field_title(source, field_name: str) -> str:
        """
        Получить наименование поля из docstring свойства @property через рефлексию
        """
        if source is None:
            return field_name

        cls = source if isinstance(source, type) else source.__class__
        attribute = getattr(cls, field_name, None)
        if isinstance(attribute, property) and attribute.__doc__:
            doc = attribute.__doc__.strip().split("\n")[0].strip()
            doc_lower = doc.lower()

            # Поиск по декларативной таблице правил
            for keyword, title in common.__title_rules:
                if keyword in doc_lower:
                    return title

            for prefix in ("Возвращает ", "Возвращает: ", "Задаёт ", "Задает "):
                if doc.startswith(prefix):
                    doc = doc[len(prefix):].strip()
            doc = doc.split(":")[0].split("(")[0].strip()
            if doc:
                return doc[0].upper() + doc[1:]

        return field_name.replace("_", " ").capitalize()
