from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Dtos.report_type_dto import report_type_enum
import connexion
import flask

api = connexion.FlaskApp(__name__, specification_dir="./")

@api.route("/", methods=["GET"])
def index():
    return """
    <h2>Сервер отчётов</h2>
    <p>Нажмите на ссылку:</p>
    <ul>
      <li><a href="/api/report?format=HTML&type=recipe&id=Сборка пасты" target="_blank">1. HTML отчёт (откроется в браузере)</a></li>
      <li><a href="/api/report?format=XML&type=recipe&id=Сборка пасты" target="_blank">2. XML отчёт (откроется структурированный XML)</a></li>
      <li><a href="/api/report?format=TXT&type=recipe&id=Сборка пасты" target="_blank">3. TXT отчёт (текстовый вид)</a></li>
      <li><a href="/api/report?format=CSV&type=recipe&id=Сборка пасты">4. CSV отчёт (скачается файл report.csv)</a></li>
      <li><a href="/api/report?format=MARKDOWN&type=recipe&id=Сборка пасты">5. Markdown отчёт (скачается файл report.md)</a></li>
      <li><a href="/api/report_default?type=recipe&id=Сборка пасты">6. Отчёт по умолчанию из настроек (create_default)</a></li>
    </ul>
    """


@api.route("/api/get_report", methods=["GET"])
def get_report():
    return "success"


def _find_entity(entity_type: str, entity_id: str):
    """Ищет сущность в хранилище по типу и коду"""
    store = storage_manager()
    if not store.is_loaded:
        store.load()

    type_map = {
        "nomenclature": store.nomenclatures,
        "unit": store.units,
        "recipe": store.recipes,
    }

    items = type_map.get(entity_type)
    if items is None:
        return None

    for item in items:
        owner_name = getattr(item, "owner", None) and item.owner.name
        if item.id == entity_id or item.name == entity_id or owner_name == entity_id:
            return item
    return None


@api.route("/api/report", methods=["GET"])
def report():
    """
    GET /api/report?format=XML&type=nomenclature&id=...
    Формирует отчёт в указанном формате для указанного типа и кода сущности
    Для CSV и Markdown — скачивание бинарного файла
    Для XML, HTML, TXT — текстовый ответ
    """
    fmt = flask.request.args.get("format", "").upper()
    entity_type = flask.request.args.get("type", "")
    entity_id = flask.request.args.get("id", "")

    if not fmt or not entity_type or not entity_id:
        return flask.jsonify({"error": "Необходимы параметры: format, type, id"}), 400

    # Проверяем формат
    try:
        report_type = report_type_enum[fmt]
    except KeyError:
        valid = [e.name for e in report_type_enum]
        return flask.jsonify({"error": f"Неизвестный формат '{fmt}'. Допустимые: {valid}"}), 400

    # Ищем сущность
    entity = _find_entity(entity_type, entity_id)
    if entity is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{entity_id}' не найдена"}), 404

    # Формируем отчёт
    factory = report_factory()
    report_obj = factory.create(report_type)
    result = report_obj.build(entity)

    # CSV и Markdown — бинарное скачивание файла
    if report_type in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        ext = "csv" if report_type == report_type_enum.CSV else "md"
        return flask.Response(
            bytes(result.binary),
            mimetype="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=report.{ext}"}
        )

    # XML, HTML, TXT — текстовый ответ
    content_types = {
        report_type_enum.XML: "application/xml",
        report_type_enum.HTML: "text/html",
        report_type_enum.TXT: "text/plain",
    }
    return flask.Response(result.text, mimetype=content_types.get(report_type, "text/plain"))


@api.route("/api/report_default", methods=["GET"])
def report_default():
    """
    GET /api/report_default?type=nomenclature&id=...
    Формирует отчёт в формате по умолчанию из настроек (create_default)
    """
    entity_type = flask.request.args.get("type", "")
    entity_id = flask.request.args.get("id", "")

    if not entity_type or not entity_id:
        return flask.jsonify({"error": "Необходимы параметры: type, id"}), 400

    entity = _find_entity(entity_type, entity_id)
    if entity is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{entity_id}' не найдена"}), 404

    factory = report_factory()
    report_obj = factory.create_default()
    result = report_obj.build(entity)

    # Определяем формат из настроек
    default_format = factory.create_default().__class__.__name__
    mgr = settings_manager()
    current_format = mgr.settings.response_format

    if current_format in (report_type_enum.CSV, report_type_enum.MARKDOWN):
        ext = "csv" if current_format == report_type_enum.CSV else "md"
        return flask.Response(
            bytes(result.binary),
            mimetype="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=report.{ext}"}
        )

    content_types = {
        report_type_enum.XML: "application/xml",
        report_type_enum.HTML: "text/html",
        report_type_enum.TXT: "text/plain",
    }
    return flask.Response(result.text, mimetype=content_types.get(current_format, "text/plain"))


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)
