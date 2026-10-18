from Src.Core.exception import arguments_exception


class common:
    """Набор общих статических методов рефлексии"""

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
