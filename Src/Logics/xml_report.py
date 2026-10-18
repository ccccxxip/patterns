import xml.etree.ElementTree as ET
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common


class xml_report(abstract_report):
    """Формирует отчёт в формате XML (текстовое представление)"""

    @property
    def mime_type(self) -> str:
        """MIME-тип содержимого отчёта"""
        return "application/xml"

    @property
    def file_extension(self) -> str:
        """Расширение файла отчёта"""
        return "xml"

    @property
    def is_attachment(self) -> bool:
        """Флаг скачивания вложения"""
        return False

    def _to_string(self, root: ET.Element) -> str:
        """Преобразует XML-дерево в строку с отступами и заголовком"""
        ET.indent(root, space="  ")
        return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(
            root, encoding="unicode", xml_declaration=False
        )

    def build(self, source: base_model) -> report_result_dto:
        """Формирует XML-отчёт для любой сущности полностью на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        root_tag = source.__class__.__name__.replace("_model", "")
        root = ET.Element(root_tag)

        # Вывод всех скалярных полей сущности через рефлексию
        for field in scalar_fields:
            if field in ("total_gross_weight", "total_net_weight"):
                continue
            val = getattr(source, field)
            val_str = self._format_value(val, source)
            ET.SubElement(root, field).text = val_str

        # Если сущность составная (табличная часть)
        if list_fields:
            for list_field in list_fields:
                items = getattr(source, list_field, [])
                items_el = ET.SubElement(root, list_field)
                for item in items:
                    item_el = ET.SubElement(items_el, "ingredient")
                    ET.SubElement(item_el, "id").text = item.id
                    ET.SubElement(item_el, "name").text = item.name
                    if hasattr(item, "gross_weight"):
                        ET.SubElement(item_el, "gross_weight").text = f"{item.gross_weight:.2f}"
                    if hasattr(item, "net_weight"):
                        ET.SubElement(item_el, "net_weight").text = f"{item.net_weight:.2f}"

            if hasattr(source, "total_gross_weight") and hasattr(source, "total_net_weight"):
                totals = ET.SubElement(root, "totals")
                ET.SubElement(totals, "total_gross").text = f"{source.total_gross_weight:.2f}"
                ET.SubElement(totals, "total_net").text = f"{source.total_net_weight:.2f}"

        result = report_result_dto()
        result.text = self._to_string(root)
        return result
