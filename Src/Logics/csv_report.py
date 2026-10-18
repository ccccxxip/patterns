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

    def build(self, source: base_model) -> report_result_dto:
        """Формирует CSV-отчёт для любой сущности полностью на основе рефлексии"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")

        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        if list_fields:
            # Составная сущность: выгрузка табличной части
            items = getattr(source, list_fields[0], [])
            writer.writerow(["Код", "Наименование", "Брутто (г)", "Нетто (г)"])
            for item in items:
                writer.writerow([
                    item.id,
                    item.name,
                    f"{getattr(item, 'gross_weight', 0):.2f}",
                    f"{getattr(item, 'net_weight', 0):.2f}"
                ])
            writer.writerow([])
            # Вывод всех итоговых скалярных полей через рефлексию
            for field in scalar_fields:
                if field in ("id", "name", "owner", "portions", "preparation_method"):
                    continue
                title = common.get_field_title(source, field)
                val_str = self._format_value(getattr(source, field), source)
                writer.writerow([title, val_str])
        else:
            # Одиночная сущность: универсальная карточка по рефлексии
            writer.writerow(["Поле", "Значение"])
            for field in scalar_fields:
                title = common.get_field_title(source, field)
                val_str = self._format_value(getattr(source, field), source)
                writer.writerow([title, val_str])

        result = report_result_dto()
        result.binary = list(output.getvalue().encode("utf-8-sig"))
        return result
