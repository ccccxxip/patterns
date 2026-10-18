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
        """Формирует HTML-отчёт для любой сущности полностью на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")

        # Универсальный вывод метаданных сущности через рефлексию
        meta_divs = ""
        for field in scalar_fields:
            if field == "name":
                continue
            title = common.get_field_title(source, field)
            val_str = self._format_value(getattr(source, field), source)
            meta_divs += f"<div class='meta'><b>{title}:</b> {val_str}</div>\n"

        body = f"<h1>{entity_title}: {source.name}</h1>\n{meta_divs}"

        # Если сущность составная (содержит списки / табличные части)
        if list_fields:
            for list_field in list_fields:
                items = getattr(source, list_field, [])
                if not items:
                    continue
                list_title = common.get_field_title(source, list_field)
                rows = ""
                for item in items:
                    rows += (
                        f"  <tr><td>{item.id}</td><td>{item.name}</td>"
                        f"<td>{getattr(item, 'gross_weight', 0):.2f}</td><td>{getattr(item, 'net_weight', 0):.2f}</td></tr>\n"
                    )
                body += (
                    f"<h2>{list_title}</h2>\n"
                    f"<table>\n"
                    f"  <tr><th>Код</th><th>Наименование</th><th>Брутто (г)</th><th>Нетто (г)</th></tr>\n"
                    f"{rows}</table>\n"
                )

        result = report_result_dto()
        result.text = self._wrap(body)
        return result
