import csv
import io
from Src.Core.abstract_report import abstract_report
from Src.Dtos.report_result_dto import report_result_dto
from Src.Core.base_model import base_model


class csv_report(abstract_report):
    """Формирует отчёт в формате CSV (бинарные данные для скачивания)"""

    def build(self, source: base_model) -> report_result_dto:
        """Формирует CSV-отчёт для переданной сущности"""
        from Src.Models.recipe_model import recipe_model
        from Src.Models.nomenclature_model import nomenclature_model
        from Src.Models.unit_model import unit_model

        if isinstance(source, recipe_model):
            text = self._build_recipe(source)
        elif isinstance(source, nomenclature_model):
            text = self._build_nomenclature(source)
        elif isinstance(source, unit_model):
            text = self._build_unit(source)
        else:
            text = f"id;name\n{source.id};{source.name}\n"

        result = report_result_dto()
        result.binary = list(text.encode("utf-8-sig"))
        return result

    def _build_recipe(self, recipe) -> str:
        """Формирует CSV-таблицу ингредиентов рецепта с итогами"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["Код", "Наименование", "Брутто (г)", "Нетто (г)"])
        for ing in recipe.ingredients:
            writer.writerow([ing.id, ing.name, f"{ing.gross_weight:.2f}", f"{ing.net_weight:.2f}"])
        writer.writerow([])
        writer.writerow(["Итого Брутто", f"{recipe.total_gross_weight:.2f}"])
        writer.writerow(["Итого Нетто", f"{recipe.total_net_weight:.2f}"])
        return output.getvalue()

    def _build_nomenclature(self, nom) -> str:
        """Формирует CSV-таблицу свойств номенклатуры"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["Поле", "Значение"])
        writer.writerow(["Код", nom.id])
        writer.writerow(["Наименование", nom.name])
        writer.writerow(["Полное наименование", nom.full_name])
        writer.writerow(["Группа", nom.group.name])
        writer.writerow(["Единица измерения", nom.unit.name])
        writer.writerow(["Тип", nom.type.name])
        return output.getvalue()

    def _build_unit(self, unit) -> str:
        """Формирует CSV-таблицу свойств единицы измерения"""
        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")
        writer.writerow(["Поле", "Значение"])
        writer.writerow(["Код", unit.id])
        writer.writerow(["Наименование", unit.name])
        writer.writerow(["Коэффициент", unit.ratio])
        base_name = unit.base_unit.name if unit.base_unit is not unit else "базовая"
        writer.writerow(["Базовая единица", base_name])
        return output.getvalue()
