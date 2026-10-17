from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class html_report(abstract_report):
    """Формирует отчёт в формате HTML (текстовое представление)"""

    def build(self, source: base_model) -> report_result_dto:
        """Формирует HTML-отчёт для переданной сущности"""
        from Src.Models.recipe_model import recipe_model
        from Src.Models.nomenclature_model import nomenclature_model
        from Src.Models.unit_model import unit_model

        if isinstance(source, recipe_model):
            body = self._build_recipe(source)
        elif isinstance(source, nomenclature_model):
            body = self._build_nomenclature(source)
        elif isinstance(source, unit_model):
            body = self._build_unit(source)
        else:
            body = f"<p><b>ID:</b> {source.id}</p><p><b>Наименование:</b> {source.name}</p>"

        result = report_result_dto()
        result.text = self._wrap(body)
        return result

    def _wrap(self, body: str) -> str:
        """Оборачивает содержимое в полный HTML-документ со стилями"""
        return (
            '<!DOCTYPE html>\n<html lang="ru">\n<head>\n'
            '  <meta charset="UTF-8">\n'
            '  <title>Отчёт</title>\n'
            '  <style>\n'
            '    body { font-family: Arial, sans-serif; margin: 2rem; }\n'
            '    table { border-collapse: collapse; width: 100%; margin-top: 1rem; }\n'
            '    th { background: #3498db; color: #fff; padding: .5rem; text-align: left; }\n'
            '    td { padding: .4rem; border-bottom: 1px solid #ddd; }\n'
            '    .meta b { display: inline-block; min-width: 220px; }\n'
            '  </style>\n'
            f'</head>\n<body>\n{body}\n</body>\n</html>'
        )

    def _build_recipe(self, recipe) -> str:
        """Формирует HTML-разметку карточки рецепта с таблицей ингредиентов"""
        rows = ""
        for ing in recipe.ingredients:
            rows += (
                f"  <tr><td>{ing.id}</td><td>{ing.name}</td>"
                f"<td>{ing.gross_weight:.2f}</td><td>{ing.net_weight:.2f}</td></tr>\n"
            )
        return (
            f"<h1>{recipe.name}</h1>\n"
            f"<div class='meta'><b>Код:</b> {recipe.id}</div>\n"
            f"<div class='meta'><b>Блюдо:</b> {recipe.owner.name}</div>\n"
            f"<div class='meta'><b>Порций:</b> {recipe.portions}</div>\n"
            f"<div class='meta'><b>Способ приготовления:</b> {recipe.preparation_method or '—'}</div>\n"
            f"<h2>Состав</h2>\n"
            f"<table>\n"
            f"  <tr><th>Код</th><th>Наименование</th><th>Брутто (г)</th><th>Нетто (г)</th></tr>\n"
            f"{rows}</table>\n"
            f"<p><b>Итого Брутто:</b> {recipe.total_gross_weight:.2f} г | "
            f"<b>Итого Нетто:</b> {recipe.total_net_weight:.2f} г</p>\n"
        )

    def _build_nomenclature(self, nom) -> str:
        """Формирует HTML-разметку карточки номенклатуры"""
        return (
            f"<h1>Номенклатура: {nom.name}</h1>\n"
            f"<div class='meta'><b>Код:</b> {nom.id}</div>\n"
            f"<div class='meta'><b>Полное наименование:</b> {nom.full_name}</div>\n"
            f"<div class='meta'><b>Группа:</b> {nom.group.name}</div>\n"
            f"<div class='meta'><b>Единица измерения:</b> {nom.unit.name}</div>\n"
            f"<div class='meta'><b>Тип:</b> {nom.type.name}</div>\n"
        )

    def _build_unit(self, unit) -> str:
        """Формирует HTML-разметку карточки единицы измерения"""
        base_name = unit.base_unit.name if unit.base_unit is not unit else "базовая"
        return (
            f"<h1>Единица измерения: {unit.name}</h1>\n"
            f"<div class='meta'><b>Код:</b> {unit.id}</div>\n"
            f"<div class='meta'><b>Коэффициент:</b> {unit.ratio}</div>\n"
            f"<div class='meta'><b>Базовая единица:</b> {base_name}</div>\n"
        )
