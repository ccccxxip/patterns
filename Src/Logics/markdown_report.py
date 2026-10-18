from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common


class markdown_report(abstract_report):
    """Формирует отчёт в формате Markdown (бинарные данные для скачивания)"""

    @property
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        return "text/markdown"

    @property
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        return "md"

    @property
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        return True

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
        """Формирует Markdown-отчёт для переданной сущности на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")

        if list_fields:
            # Сущность с табличной частью (технологическая карта)
            lines = [
                f"# {entity_title}: {source.name}",
                "",
                f"**Код:** `{source.id}`",
                f"**Блюдо:** {getattr(source.owner, 'name', source.name)}",
                f"**Порций:** {getattr(source, 'portions', '')}",
                f"**Способ приготовления:** {getattr(source, 'preparation_method', None) or '—'}",
                "",
                "## Состав",
                "",
                "| Код | Наименование | Брутто (г) | Нетто (г) |",
                "|-----|-------------|-----------|----------|",
            ]
            items = getattr(source, list_fields[0], [])
            for ing in items:
                lines.append(
                    f"| `{ing.id}` | {ing.name} | {ing.gross_weight:.2f} | {ing.net_weight:.2f} |"
                )
            if hasattr(source, "total_gross_weight") and hasattr(source, "total_net_weight"):
                lines += [
                    "",
                    f"**Итого Брутто:** {source.total_gross_weight:.2f} г",
                    f"**Итого Нетто:** {source.total_net_weight:.2f} г",
                ]
        else:
            # Универсальная карточка сущности
            lines = [
                f"# {entity_title}: {source.name}",
                "",
            ]
            for field in scalar_fields:
                title = self.__field_titles.get(field, field)
                val_str = self._format_value(getattr(source, field), source)
                lines.append(f"**{title}:** {val_str}")

        text = "\n".join(lines)
        result = report_result_dto()
        result.binary = list(text.encode("utf-8"))
        return result
