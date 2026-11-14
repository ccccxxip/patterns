import flask
import connexion
from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Logics.convert_factory import convert_factory
from Src.Logics.mapping_factory import mapping_factory
from Src.Core.validator import operation_exception
from Src.Core.exception import arguments_exception
from Src.Dtos.report_type_dto import report_type_enum

api = connexion.FlaskApp(__name__, specification_dir="./")

store = storage_manager()
converter = convert_factory()
mapping = mapping_factory()


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
    """GET /api/report?format=XML&type=recipe&id=..."""
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
    """GET /api/report_default?type=recipe&id=..."""
    entity_type = flask.request.args.get("type", "")
    entity_id = flask.request.args.get("id", "")

    if not entity_type or not entity_id:
        return flask.jsonify({"error": "Необходимы параметры: type, id"}), 400

    entity = store.get_entity(entity_type, entity_id)
    if entity is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{entity_id}' не найдена"}), 404

    factory = report_factory()
    report_cls = factory.create_default()
    report_obj = report_cls()
    result = report_obj.build(entity)

    return _build_response(report_obj, result)


# Обработчики для OpenAPI / Swagger

def get_report_formats():
    """GET /api/reports/formats — список всех форматов отчетов в JSON"""
    formats = [item.name for item in report_type_enum]
    return flask.jsonify(formats), 200


def get_report_formats_alias():
    """GET /api/get_report_formats — алиас для получения форматов отчетов"""
    return get_report_formats()


def get_entities():
    """GET /api/get_entities — список доступных типов доменных сущностей"""
    types = list(store.data.keys())
    return flask.jsonify(types), 200


def get_entities_by_type(entity_type: str):
    """GET /api/entities/{entity_type} — список сущностей указанного типа"""
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    items = store.get_entities_by_type(k)
    converted = [converter.Convert(item) for item in items]
    return flask.jsonify(converted), 200


def get_entity_by_id(entity_type: str, id: str):
    """GET /api/entities/{entity_type}/{id} — получить сущность по ID"""
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    item = store.get_entity(k, id)
    if item is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    return flask.jsonify(converter.Convert(item)), 200


def create_entity(entity_type: str, body: dict = None):
    """POST /api/entities/{entity_type} — добавить новую сущность"""
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    data = body if body is not None else (flask.request.get_json(silent=True) or {})
    try:
        model = mapping.deserialize(k, data)
        store.add_entity(k, model)
        return flask.jsonify(converter.Convert(model)), 201
    except (operation_exception, arguments_exception) as ex:
        return flask.jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return flask.jsonify({"error": f"Внутренняя ошибка: {ex}"}), 400


def update_entity(entity_type: str, id: str, body: dict = None):
    """PUT /api/entities/{entity_type}/{id} — обновить существующую сущность"""
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    existing = store.get_entity(k, id)
    if existing is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    data = body if body is not None else (flask.request.get_json(silent=True) or {})
    try:
        model = mapping.deserialize(k, data)
        store.update_entity(k, id, model)
        return flask.jsonify(converter.Convert(model)), 200
    except (operation_exception, arguments_exception) as ex:
        return flask.jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return flask.jsonify({"error": f"Внутренняя ошибка: {ex}"}), 400


def patch_entity(entity_type: str, id: str, body: dict = None):
    """PATCH /api/entities/{entity_type}/{id} — частично обновить существующую сущность"""
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    existing = store.get_entity(k, id)
    if existing is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    data = body if body is not None else (flask.request.get_json(silent=True) or {})
    try:
        # Текущее состояние сущности объединяем с переданными новыми полями
        current_data = converter.Convert(existing)
        if isinstance(current_data, dict):
            current_data.update(data)
        else:
            current_data = data

        model = mapping.deserialize(k, current_data)
        store.update_entity(k, id, model)
        return flask.jsonify(converter.Convert(model)), 200
    except (operation_exception, arguments_exception) as ex:
        return flask.jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return flask.jsonify({"error": f"Внутренняя ошибка: {ex}"}), 400


def delete_entity(entity_type: str, id: str):
    """DELETE /api/entities/{entity_type}/{id} — удалить сущность"""
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    existing = store.get_entity(k, id)
    if existing is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    try:
        store.delete_entity(k, id)
        return flask.jsonify({"result": "success"}), 200
    except operation_exception as ex:
        return flask.jsonify({"error": str(ex)}), 400


# Подключаем спецификацию
api.add_api("openapi.yaml")


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=8080)