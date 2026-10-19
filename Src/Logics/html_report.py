from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model


class html_report(abstract_report):
    """Формирует отчёт в формате HTML (текстовое представление)"""

    def __init__(self):
        super().__init__()
        # Связка конкретного составного типа с внутренним методом
        self.register(recipe_model, self._build_recipe)

    @property
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        return "text/html"

    @property
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        return "html"

    @property
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        return False

    __entity_titles = {
        "recipe_model": "Технологическая карта",
        "nomenclature_model": "Номенклатура",
        "unit_model": "Единица измерения",
    }

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

    def _build_recipe(self, recipe: recipe_model) -> report_result_dto:
        """Специализированный построитель HTML-отчёта для технологической карты"""
        rows = ""
        for item in recipe.ingredients:
            rows += (
                f"  <tr><td>{item.id}</td><td>{item.name}</td>"
                f"<td>{item.gross_weight:.2f}</td><td>{item.net_weight:.2f}</td></tr>\n"
            )

        body = (
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

        result = report_result_dto()
        result.text = self._wrap(body)
        return result

    def _build_generic(self, source: base_model) -> report_result_dto:
        """Универсальный построитель HTML для любой сущности на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        meta_divs = ""
        for field in scalar_fields:
            if field == "name":
                continue
            title = common.get_field_title(source, field)
            val_str = self._format_value(getattr(source, field), source)
            meta_divs += f"<div class='meta'><b>{title}:</b> {val_str}</div>\n"

        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")
        body = f"<h1>{entity_title}: {source.name}</h1>\n{meta_divs}"

        result = report_result_dto()
        result.text = self._wrap(body)
        return result
