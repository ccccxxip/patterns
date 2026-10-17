import xml.etree.ElementTree as ET
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class xml_report(abstract_report):
    """Формирует отчёт в формате XML (текстовое представление)"""

    def build(self, source: base_model) -> report_result_dto:
        """Формирует XML-отчёт для переданной сущности"""
        from Src.Models.recipe_model import recipe_model
        from Src.Models.nomenclature_model import nomenclature_model
        from Src.Models.unit_model import unit_model

        if isinstance(source, recipe_model):
            xml_str = self._build_recipe(source)
        elif isinstance(source, nomenclature_model):
            xml_str = self._build_nomenclature(source)
        elif isinstance(source, unit_model):
            xml_str = self._build_unit(source)
        else:
            root = ET.Element("entity")
            ET.SubElement(root, "id").text = source.id
            ET.SubElement(root, "name").text = source.name
            xml_str = self._to_string(root)

        result = report_result_dto()
        result.text = xml_str
        return result

    def _to_string(self, root: ET.Element) -> str:
        """Преобразует XML-дерево в строку с отступами и заголовком"""
        ET.indent(root, space="  ")
        return '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(
            root, encoding="unicode", xml_declaration=False
        )

    def _build_recipe(self, recipe) -> str:
        """Формирует текст XML-отчёта для рецепта (технологической карты)"""
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
        return self._to_string(root)

    def _build_nomenclature(self, nom) -> str:
        """Формирует текст XML-отчёта для номенклатуры"""
        root = ET.Element("nomenclature")
        ET.SubElement(root, "id").text = nom.id
        ET.SubElement(root, "name").text = nom.name
        ET.SubElement(root, "full_name").text = nom.full_name
        ET.SubElement(root, "group").text = nom.group.name
        ET.SubElement(root, "unit").text = nom.unit.name
        ET.SubElement(root, "type").text = nom.type.name
        return self._to_string(root)

    def _build_unit(self, unit) -> str:
        """Формирует текст XML-отчёта для единицы измерения"""
        root = ET.Element("unit")
        ET.SubElement(root, "id").text = unit.id
        ET.SubElement(root, "name").text = unit.name
        ET.SubElement(root, "ratio").text = str(unit.ratio)
        base_name = unit.base_unit.name if unit.base_unit is not unit else "базовая"
        ET.SubElement(root, "base_unit").text = base_name
        return self._to_string(root)
