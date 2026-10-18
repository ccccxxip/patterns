import csv
import io
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common


class csv_report(abstract_report):
    """Формирует отчёт в формате CSV (бинарные данные для скачивания)"""

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
        "total_gross_weight": "Итого Брутто",
        "total_net_weight": "Итого Нетто",
        "gross_weight": "Брутто (г)",
        "net_weight": "Нетто (г)",
    }

    def build(self, source: base_model) -> report_result_dto:
        """Формирует CSV-отчёт для переданной сущности на основе рефлексии"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")

        # Получаем скалярные поля и свойства-списки через рефлексию
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        if list_fields:
            # Сущность с табличной частью (например, рецепт со списком ингредиентов)
            items = getattr(source, list_fields[0], [])
            writer.writerow(["Код", "Наименование", "Брутто (г)", "Нетто (г)"])
            for item in items:
                writer.writerow([
                    item.id,
                    item.name,
                    f"{item.gross_weight:.2f}",
                    f"{item.net_weight:.2f}"
                ])
            writer.writerow([])
            if hasattr(source, "total_gross_weight"):
                writer.writerow(["Итого Брутто", f"{source.total_gross_weight:.2f}"])
            if hasattr(source, "total_net_weight"):
                writer.writerow(["Итого Нетто", f"{source.total_net_weight:.2f}"])
        else:
            # Универсальная карточка для любой одиночной сущности
            writer.writerow(["Поле", "Значение"])
            for field in scalar_fields:
                title = self.__field_titles.get(field, field)
                val_str = self._format_value(getattr(source, field), source)
                writer.writerow([title, val_str])

        result = report_result_dto()
        result.binary = list(output.getvalue().encode("utf-8-sig"))
        return result
