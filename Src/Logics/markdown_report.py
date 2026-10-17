from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class markdown_report(abstract_report):
    """Формирует отчёт в формате Markdown (бинарные данные для скачивания)"""

    def build(self, source: base_model) -> report_result_dto:
        """Формирует Markdown-отчёт для переданной сущности"""
        from Src.Models.recipe_model import recipe_model
        from Src.Models.nomenclature_model import nomenclature_model
        from Src.Models.unit_model import unit_model

        if isinstance(source, recipe_model):
            text = self._build_recipe(source)
        elif isinstance(source, nomenclature_model):
            text = self._build_nomenclature(source)
        elif isinstance(source, unit_model):
            text = self._build_unit(source)
        else:
            text = f"# Отчёт\n\n**ID:** {source.id}\n\n**Наименование:** {source.name}\n"

        result = report_result_dto()
        result.binary = list(text.encode("utf-8"))
        return result

    def _build_recipe(self, recipe) -> str:
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
        for ing in recipe.ingredients:
            lines.append(
                f"| `{ing.id}` | {ing.name} | {ing.gross_weight:.2f} | {ing.net_weight:.2f} |"
            )
        lines += [
            "",
            f"**Итого Брутто:** {recipe.total_gross_weight:.2f} г",
            f"**Итого Нетто:** {recipe.total_net_weight:.2f} г",
        ]
        return "\n".join(lines)

    def _build_nomenclature(self, nom) -> str:
        lines = [
            f"# Номенклатура: {nom.name}",
            "",
            f"**Код:** `{nom.id}`",
            f"**Полное наименование:** {nom.full_name}",
            f"**Группа:** {nom.group.name}",
            f"**Единица измерения:** {nom.unit.name}",
            f"**Тип:** {nom.type.name}",
        ]
        return "\n".join(lines)

    def _build_unit(self, unit) -> str:
        base_name = unit.base_unit.name if unit.base_unit is not unit else "базовая"
        lines = [
            f"# Единица измерения: {unit.name}",
            "",
            f"**Код:** `{unit.id}`",
            f"**Коэффициент:** {unit.ratio}",
            f"**Базовая единица:** {base_name}",
        ]
        return "\n".join(lines)
