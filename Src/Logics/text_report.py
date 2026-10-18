from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common


class text_report(abstract_report):
    """Формирует отчёт в простом текстовом формате"""

    @property
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        return "text/plain"

    @property
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        return "txt"

    @property
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        return False

    __entity_titles = {
        "recipe_model": "Технологическая карта",
        "nomenclature_model": "Номенклатура",
        "unit_model": "Единица измерения",
    }

    def build(self, source: base_model) -> report_result_dto:
        """Формирует текстовый отчёт для любой сущности полностью на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        entity_title = self.__entity_titles.get(source.__class__.__name__, "Отчёт")

        lines = [f"{entity_title}: {source.name}"]

        # Вывод всех метаданных через рефлексию
        for field in scalar_fields:
            if field == "name":
                continue
            title = common.get_field_title(source, field)
            val_str = self._format_value(getattr(source, field), source)
            lines.append(f"{title}: {val_str}")

        # Если сущность составная
        if list_fields:
            for list_field in list_fields:
                items = getattr(source, list_field, [])
                if not items:
                    continue
                list_title = common.get_field_title(source, list_field)
                lines += [
                    "",
                    f"{list_title}:",
                    "Код | Наименование | Брутто (г) | Нетто (г)",
                    "-" * 50,
                ]
                for item in items:
                    lines.append(
                        f"{item.id} | {item.name} | {getattr(item, 'gross_weight', 0):.2f} | {getattr(item, 'net_weight', 0):.2f}"
                    )
                lines.append("-" * 50)

        result = report_result_dto()
        result.text = "\n".join(lines) + "\n"
        return result
