from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common


class html_report(abstract_report):
    """Формирует отчёт в формате HTML (текстовое представление)"""

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

    def build(self, source: base_model) -> report_result_dto:
        """Формирует HTML-отчёт для переданной сущности на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")

        if list_fields:
            # Сущность с табличной частью (рецепт)
            rows = ""
            items = getattr(source, list_fields[0], [])
            for ing in items:
                rows += (
                    f"  <tr><td>{ing.id}</td><td>{ing.name}</td>"
                    f"<td>{ing.gross_weight:.2f}</td><td>{ing.net_weight:.2f}</td></tr>\n"
                )

            body = (
                f"<h1>{source.name}</h1>\n"
                f"<div class='meta'><b>Код:</b> {source.id}</div>\n"
                f"<div class='meta'><b>Блюдо:</b> {getattr(source.owner, 'name', source.name)}</div>\n"
                f"<div class='meta'><b>Порций:</b> {getattr(source, 'portions', '')}</div>\n"
                f"<div class='meta'><b>Способ приготовления:</b> {getattr(source, 'preparation_method', None) or '—'}</div>\n"
                f"<h2>Состав</h2>\n"
                f"<table>\n"
                f"  <tr><th>Код</th><th>Наименование</th><th>Брутто (г)</th><th>Нетто (г)</th></tr>\n"
                f"{rows}</table>\n"
            )
            if hasattr(source, "total_gross_weight") and hasattr(source, "total_net_weight"):
                body += (
                    f"<p><b>Итого Брутто:</b> {source.total_gross_weight:.2f} г | "
                    f"<b>Итого Нетто:</b> {source.total_net_weight:.2f} г</p>\n"
                )
        else:
            # Одиночная сущность
            meta_divs = ""
            for field in scalar_fields:
                title = self.__field_titles.get(field, field)
                val_str = self._format_value(getattr(source, field), source)
                meta_divs += f"<div class='meta'><b>{title}:</b> {val_str}</div>\n"

            body = f"<h1>{entity_title}: {source.name}</h1>\n{meta_divs}"

        result = report_result_dto()
        result.text = self._wrap(body)
        return result
