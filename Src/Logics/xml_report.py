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
        """Формирует XML-отчёт для переданной сущности на основе рефлексии"""
        scalar_fields = common.get_fields(source, is_common=True)
        all_fields = common.get_fields(source, is_common=False)
        list_fields = [f for f in all_fields if f not in scalar_fields]

        root_tag = source.__class__.__name__.replace("_model", "")
        root = ET.Element(root_tag)

        if list_fields:
            # Сущность с табличной частью (рецепт)
            ET.SubElement(root, "id").text = source.id
            ET.SubElement(root, "name").text = source.name
            ET.SubElement(root, "owner").text = getattr(source.owner, "name", source.name)
            ET.SubElement(root, "portions").text = str(getattr(source, "portions", ""))
            ET.SubElement(root, "preparation_method").text = getattr(source, "preparation_method", None) or ""

            ingredients_el = ET.SubElement(root, "ingredients")
            items = getattr(source, list_fields[0], [])
            for ing in items:
                ing_el = ET.SubElement(ingredients_el, "ingredient")
                ET.SubElement(ing_el, "id").text = ing.id
                ET.SubElement(ing_el, "name").text = ing.name
                ET.SubElement(ing_el, "gross_weight").text = f"{ing.gross_weight:.2f}"
                ET.SubElement(ing_el, "net_weight").text = f"{ing.net_weight:.2f}"

            if hasattr(source, "total_gross_weight") and hasattr(source, "total_net_weight"):
                totals = ET.SubElement(root, "totals")
                ET.SubElement(totals, "total_gross").text = f"{source.total_gross_weight:.2f}"
                ET.SubElement(totals, "total_net").text = f"{source.total_net_weight:.2f}"
        else:
            # Одиночная сущность: заполняем все поля через рефлексию
            for field in scalar_fields:
                val = getattr(source, field)
                val_str = self._format_value(val, source)
                ET.SubElement(root, field).text = val_str

        result = report_result_dto()
        result.text = self._to_string(root)
        return result
