import csv
import io
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model


class csv_report(abstract_report):
    """Формирует отчёт в формате CSV (бинарные данные для скачивания)"""

    def __init__(self):
        super().__init__()
        # Связка конкретного типа с внутренним методом
        self.register(recipe_model, self._build_recipe)

    @property
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        return "text/csv"

    @property
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        return "csv"

    @property
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        return True

    def _build_recipe(self, recipe: recipe_model) -> report_result_dto:
        """Специализированный построитель отчёта для технологической карты"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")

        writer.writerow(["Код", "Наименование", "Брутто (г)", "Нетто (г)"])
        for item in recipe.ingredients:
            writer.writerow([
                item.id,
                item.name,
                f"{item.gross_weight:.2f}",
                f"{item.net_weight:.2f}"
            ])
        writer.writerow([])
        writer.writerow(["Итого Брутто", f"{recipe.total_gross_weight:.2f}"])
        writer.writerow(["Итого Нетто", f"{recipe.total_net_weight:.2f}"])

        result = report_result_dto()
        result.binary = list(output.getvalue().encode("utf-8-sig"))
        return result

    def _build_generic(self, source: base_model) -> report_result_dto:
        """Универсальный построитель CSV для любой сущности на основе рефлексии"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")

        scalar_fields = common.get_fields(source, is_common=True)
        writer.writerow(["Поле", "Значение"])
        for field in scalar_fields:
            title = common.get_field_title(source, field)
            val_str = self._format_value(getattr(source, field), source)
            writer.writerow([title, val_str])

        result = report_result_dto()
        result.binary = list(output.getvalue().encode("utf-8-sig"))
        return result
