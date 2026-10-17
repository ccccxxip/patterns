from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class text_report(abstract_report):
    """Формирует отчёт в простом текстовом формате"""

    def build(self, source: base_model) -> report_result_dto:
        """Формирует текстовый отчёт для переданной сущности"""
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
            text = f"Код: {source.id}\nНаименование: {source.name}\n"

        result = report_result_dto()
        result.text = text
        return result

    def _build_recipe(self, recipe) -> str:
        """Формирует текст отчёта для рецепта (технологической карты)"""
        lines = [
            f"Технологическая карта: {recipe.name}",
            f"Код: {recipe.id}",
            f"Блюдо: {recipe.owner.name}",
            f"Порций: {recipe.portions}",
            f"Способ приготовления: {recipe.preparation_method or '—'}",
            "",
            "Код | Наименование | Брутто (г) | Нетто (г)",
            "-" * 50,
        ]
        for ing in recipe.ingredients:
            lines.append(f"{ing.id} | {ing.name} | {ing.gross_weight:.2f} | {ing.net_weight:.2f}")
        lines.append("-" * 50)
        lines.append(f"Итого Брутто: {recipe.total_gross_weight:.2f} г")
        lines.append(f"Итого Нетто: {recipe.total_net_weight:.2f} г")
        return "\n".join(lines)

    def _build_nomenclature(self, nom) -> str:
        """Формирует текст отчёта для номенклатуры"""
        return (
            f"Номенклатура: {nom.name}\n"
            f"Код: {nom.id}\n"
            f"Полное наименование: {nom.full_name}\n"
            f"Группа: {nom.group.name}\n"
            f"Единица измерения: {nom.unit.name}\n"
            f"Тип: {nom.type.name}\n"
        )

    def _build_unit(self, unit) -> str:
        """Формирует текст отчёта для единицы измерения"""
        base_name = unit.base_unit.name if unit.base_unit is not unit else "базовая"
        return (
            f"Единица измерения: {unit.name}\n"
            f"Код: {unit.id}\n"
            f"Коэффициент: {unit.ratio}\n"
            f"Базовая единица: {base_name}\n"
        )
