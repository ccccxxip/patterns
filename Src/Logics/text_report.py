from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common


class text_report(abstract_report):
    """Формирует отчёт в простом текстовом формате"""

    @property
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        return "text/plain"

    @property
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        return "txt"

    @property
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        return False

    __field_titles = {
        "id": "Код",
        "name": "Наименование",
        "full_name": "Полное наименование",
        "group": "Группа",
        "unit": "Единица измерения",
        "type": "Тип",
        "ratio": "Коэффициент",
        "base_unit": "Базовая единица",
        "owner": "Блюдо",
        "portions": "Порций",
        "preparation_method": "Способ приготовления",
    }

    __entity_titles = {
        "recipe_model": "Технологическая карта",
        "nomenclature_model": "Номенклатура",
        "unit_model": "Единица измерения",
    }

    def build(self, source: base_model) -> report_result_dto:
        """Формирует текстовый отчёт для переданной сущности на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")

        if list_fields:
            # Сущность с табличной частью (рецепт)
            lines = [
                f"{entity_title}: {source.name}",
                f"Код: {source.id}",
                f"Блюдо: {getattr(source.owner, 'name', source.name)}",
                f"Порций: {getattr(source, 'portions', '')}",
                f"Способ приготовления: {getattr(source, 'preparation_method', None) or '—'}",
                "",
                "Код | Наименование | Брутто (г) | Нетто (г)",
                "-" * 50,
            ]
            items = getattr(source, list_fields[0], [])
            for ing in items:
                lines.append(f"{ing.id} | {ing.name} | {ing.gross_weight:.2f} | {ing.net_weight:.2f}")
            lines.append("-" * 50)
            if hasattr(source, "total_gross_weight"):
                lines.append(f"Итого Брутто: {source.total_gross_weight:.2f} г")
            if hasattr(source, "total_net_weight"):
                lines.append(f"Итого Нетто: {source.total_net_weight:.2f} г")
            text = "\n".join(lines)
        else:
            # Одиночная сущность
            lines = [f"{entity_title}: {source.name}"]
            for field in scalar_fields:
                if field == "name":
                    continue
                title = self.__field_titles.get(field, field)
                val_str = self._format_value(getattr(source, field), source)
                lines.append(f"{title}: {val_str}")
            text = "\n".join(lines) + "\n"

        result = report_result_dto()
        result.text = text
        return result
