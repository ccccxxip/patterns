import xml.etree.ElementTree as ET
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model
from Src.Core.common import common
from Src.Models.recipe_model import recipe_model


class xml_report(abstract_report):
    """Формирует отчёт в формате XML (текстовое представление)"""

    def __init__(self):
        super().__init__()
        # Связка конкретного составного типа с внутренним методом
        self.register(recipe_model, self._build_recipe)

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

    def _build_recipe(self, recipe: recipe_model) -> report_result_dto:
        """Специализированный построитель XML для технологической карты"""
        root = ET.Element("recipe")
        ET.SubElement(root, "id").text = recipe.id
        ET.SubElement(root, "name").text = recipe.name
        ET.SubElement(root, "owner").text = recipe.owner.name
        ET.SubElement(root, "portions").text = str(recipe.portions)
        ET.SubElement(root, "preparation_method").text = recipe.preparation_method or ""

        ingredients_el = ET.SubElement(root, "ingredients")
        for ing in recipe.ingredients:
            ing_el = ET.SubElement(ingredients_el, "ingredient")
            ET.SubElement(ing_el, "id").text = ing.id
            ET.SubElement(ing_el, "name").text = ing.name
            ET.SubElement(ing_el, "gross_weight").text = f"{ing.gross_weight:.2f}"
            ET.SubElement(ing_el, "net_weight").text = f"{ing.net_weight:.2f}"

        totals = ET.SubElement(root, "totals")
        ET.SubElement(totals, "total_gross").text = f"{recipe.total_gross_weight:.2f}"
        ET.SubElement(totals, "total_net").text = f"{recipe.total_net_weight:.2f}"

        result = report_result_dto()
        result.text = self._to_string(root)
        return result

    def _build_generic(self, source: base_model) -> report_result_dto:
        """Универсальный построитель XML для любой сущности на основе рефлексии"""
        root_tag = source.__class__.__name__.replace("_model", "")
        root = ET.Element(root_tag)

        scalar_fields = common.get_fields(source, is_common=True)
        for field in scalar_fields:
            val = getattr(source, field)
            val_str = self._format_value(val, source)
            ET.SubElement(root, field).text = val_str

        result = report_result_dto()
        result.text = self._to_string(root)
        return result
