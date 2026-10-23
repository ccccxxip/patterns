from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Dtos.report_type_dto import report_type_enum
import connexion
import flask

api = connexion.FlaskApp(__name__, specification_dir="./")


@api.route("/", methods=["GET"])
def index():
    """Главная страница сервера с интерактивными ссылками на примеры отчётов"""
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
    """Тестовый маршрут для проверки работоспособности сервиса"""
    return "success"


def _build_response(report_obj, result):
    """Универсальное формирование HTTP-ответа на основе метаданных отчёта"""
    headers = {}
    if report_obj.is_attachment:
        headers["Content-Disposition"] = f"attachment; filename=report.{report_obj.file_extension}"
        body = bytes(result.binary)
    else:
        body = result.text

    return flask.Response(body, mimetype=report_obj.mime_type, headers=headers)


@api.route("/api/report", methods=["GET"])
def report():
    """
    GET /api/report?format=XML&type=nomenclature&id=...
    Формирует отчёт в указанном формате для указанной сущности
    """
    fmt = flask.request.args.get("format", "").upper()
    entity_type = flask.request.args.get("type", "")
    entity_id = flask.request.args.get("id", "")

    if not fmt or not entity_type or not entity_id:
        return flask.jsonify({"error": "Необходимы параметры: format, type, id"}), 400

    try:
        report_type = report_type_enum[fmt]
    except KeyError:
        valid = [e.name for e in report_type_enum]
        return flask.jsonify({"error": f"Неизвестный формат '{fmt}'. Допустимые: {valid}"}), 400

    store = storage_manager()
    entity = store.get_entity(entity_type, entity_id)
    if entity is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{entity_id}' не найдена"}), 404

    factory = report_factory()
    report_cls = factory.create(report_type)
    report_obj = report_cls()
    result = report_obj.build(entity)

    return _build_response(report_obj, result)


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

    store = storage_manager()
    entity = store.get_entity(entity_type, entity_id)
    if entity is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{entity_id}' не найдена"}), 404

    factory = report_factory()
    report_cls = factory.create_default()
    report_obj = report_cls()
    result = report_obj.build(entity)

    return _build_response(report_obj, result)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)
