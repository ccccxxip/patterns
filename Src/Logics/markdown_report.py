from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model


class markdown_report(abstract_report):
    """Формирует отчёт в формате Markdown (бинарные данные для скачивания)"""

    def __init__(self):
        super().__init__()
        # Связка конкретного составного типа с внутренним методом
        self.register(recipe_model, self._build_recipe)

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

    __entity_titles = {
        "recipe_model": "Технологическая карта",
        "nomenclature_model": "Номенклатура",
        "unit_model": "Единица измерения",
    }

    def _build_recipe(self, recipe: recipe_model) -> report_result_dto:
        """Специализированный построитель Markdown-отчёта для технологической карты"""
        lines = [
            f"# Технологическая карта: {recipe.name}",
            "",
            f"**Код:** `{recipe.id}`",
            f"**Блюдо:** {recipe.owner.name}",
            f"**Порций:** {recipe.portions}",
            f"**Способ приготовления:** {recipe.preparation_method or '—'}",
            "",
            "## Состав",
            "",
            "| Код | Наименование | Брутто (г) | Нетто (г) |",
            "|-----|-------------|-----------|----------|",
        ]
        for item in recipe.ingredients:
            lines.append(
                f"| `{item.id}` | {item.name} | {item.gross_weight:.2f} | {item.net_weight:.2f} |"
            )
        lines += [
            "",
            f"**Итого Брутто:** {recipe.total_gross_weight:.2f} г",
            f"**Итого Нетто:** {recipe.total_net_weight:.2f} г",
        ]

        text = "\n".join(lines)
        result = report_result_dto()
        result.binary = list(text.encode("utf-8"))
        return result

    def _build_generic(self, source: base_model) -> report_result_dto:
        """Универсальный построитель Markdown для любой сущности на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")

        lines = [
            f"# {entity_title}: {source.name}",
            "",
        ]
        for field in scalar_fields:
            if field == "name":
                continue
            title = common.get_field_title(source, field)
            val_str = self._format_value(getattr(source, field), source)
            lines.append(f"**{title}:** {val_str}")

        text = "\n".join(lines)
        result = report_result_dto()
        result.binary = list(text.encode("utf-8"))
        return result
