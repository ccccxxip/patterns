import flask
import connexion
from Src.Logics.storage_manager import storage_manager
from Src.Logics.report_factory import report_factory
from Src.Logics.convert_factory import convert_factory
from Src.Logics.mapping_factory import mapping_factory
from Src.Core.validator import operation_exception
from Src.Core.exception import arguments_exception
from Src.Dtos.report_type_dto import report_type_enum
from Src.Dtos.warehouse_dto import warehouse_dto
from Src.Dtos.unit_dto import unit_dto
from Src.Dtos.nomenclature_group_dto import nomenclature_group_dto
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.recipe_dto import recipe_dto

api = connexion.FlaskApp(__name__, specification_dir="./")


@api.route("/", methods=["GET"])
def index():
    """Главная страница сервера с интерактивными ссылками"""
    return """
    <h2>Сервер отчётов и REST API ООО &laquo;Ромашка&raquo;</h2>
    <p>Документация и тестирование API: <a href="/ui/" target="_blank"><b>Swagger UI (/ui/)</b></a></p>
    <hr>
    <p>Примеры отчетов:</p>
    <ul>
      <li><a href="/api/reports/formats" target="_blank">Форматы отчетов (JSON)</a></li>
      <li><a href="/api/report?format=HTML&type=recipe&id=Сборка пасты" target="_blank">1. HTML отчёт</a></li>
      <li><a href="/api/report?format=XML&type=recipe&id=Сборка пасты" target="_blank">2. XML отчёт</a></li>
      <li><a href="/api/report?format=TXT&type=recipe&id=Сборка пасты" target="_blank">3. TXT отчёт</a></li>
      <li><a href="/api/report?format=CSV&type=recipe&id=Сборка пасты">4. CSV отчёт (скачать)</a></li>
      <li><a href="/api/report?format=MARKDOWN&type=recipe&id=Сборка пасты">5. Markdown отчёт (скачать)</a></li>
      <li><a href="/api/report_default?type=recipe&id=Сборка пасты">6. Отчёт по умолчанию (create_default)</a></li>
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
    """GET /api/report_default?type=recipe&id=..."""
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


# Обработчики для OpenAPI / Swagger

def _get_dto_class(normalized_key: str):
    """Словарь соответствия ключа сущности и класса DTO"""
    dto_map = {
        "warehouse": warehouse_dto,
        "unit": unit_dto,
        "group": nomenclature_group_dto,
        "nomenclature": nomenclature_dto,
        "recipe": recipe_dto,
    }
    return dto_map.get(normalized_key)


def get_report_formats():
    """GET /api/reports/formats — список всех форматов отчетов в JSON"""
    formats = [item.name for item in report_type_enum]
    return flask.jsonify(formats), 200


def get_report_formats_alias():
    """GET /api/get_report_formats — алиас для получения форматов отчетов"""
    return get_report_formats()


def get_entities():
    """GET /api/get_entities — список доступных типов доменных сущностей"""
    store = storage_manager()
    types = list(store.data.keys())
    return flask.jsonify(types), 200


def get_entities_by_type(entity_type: str):
    """GET /api/entities/{entity_type} — список сущностей указанного типа"""
    store = storage_manager()
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    items = store.get_entities_by_type(k)
    cf = convert_factory()
    converted = [cf.Convert(item) for item in items]
    return flask.jsonify(converted), 200


def get_entity_by_id(entity_type: str, id: str):
    """GET /api/entities/{entity_type}/{id} — получить сущность по ID"""
    store = storage_manager()
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    item = store.get_entity(k, id)
    if item is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    cf = convert_factory()
    return flask.jsonify(cf.Convert(item)), 200


def create_entity(entity_type: str, body: dict = None):
    """POST /api/entities/{entity_type} — добавить новую сущность"""
    store = storage_manager()
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    data = body if body is not None else (flask.request.get_json(silent=True) or {})
    dto_cls = _get_dto_class(k)
    if not dto_cls:
        return flask.jsonify({"error": f"Не найден DTO для типа '{entity_type}'"}), 400

    try:
        dto = dto_cls.from_dict(data)
        if dto is None:
            return flask.jsonify({"error": "Некорректные данные для создания сущности"}), 400

        model = mapping_factory().to_model(dto)
        store.add_entity(k, model)
        cf = convert_factory()
        return flask.jsonify(cf.Convert(model)), 201
    except (operation_exception, arguments_exception) as ex:
        return flask.jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return flask.jsonify({"error": f"Внутренняя ошибка: {ex}"}), 400


def update_entity(entity_type: str, id: str, body: dict = None):
    """PUT /api/entities/{entity_type}/{id} — обновить существующую сущность"""
    store = storage_manager()
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    existing = store.get_entity(k, id)
    if existing is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    data = body if body is not None else (flask.request.get_json(silent=True) or {})
    dto_cls = _get_dto_class(k)
    if not dto_cls:
        return flask.jsonify({"error": f"Не найден DTO для типа '{entity_type}'"}), 400

    try:
        dto = dto_cls.from_dict(data)
        if dto is None:
            return flask.jsonify({"error": "Некорректные данные для обновления сущности"}), 400

        model = mapping_factory().to_model(dto)
        store.update_entity(k, id, model)
        cf = convert_factory()
        return flask.jsonify(cf.Convert(model)), 200
    except (operation_exception, arguments_exception) as ex:
        return flask.jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return flask.jsonify({"error": f"Внутренняя ошибка: {ex}"}), 400


def patch_entity(entity_type: str, id: str, body: dict = None):
    """PATCH /api/entities/{entity_type}/{id} — частично обновить существующую сущность"""
    store = storage_manager()
    k = store.normalize_key(entity_type)
    if k not in store.data:
        return flask.jsonify({"error": f"Неизвестный тип сущности '{entity_type}'"}), 400

    existing = store.get_entity(k, id)
    if existing is None:
        return flask.jsonify({"error": f"Сущность типа '{entity_type}' с id '{id}' не найдена"}), 404

    data = body if body is not None else (flask.request.get_json(silent=True) or {})
    dto_cls = _get_dto_class(k)
    if not dto_cls:
        return flask.jsonify({"error": f"Не найден DTO для типа '{entity_type}'"}), 400

    try:
        # Текущее состояние сущности объединяем с переданными новыми полями
        current_data = convert_factory().Convert(existing)
        if isinstance(current_data, dict):
            current_data.update(data)
        else:
            current_data = data

        dto = dto_cls.from_dict(current_data)
        if dto is None:
            return flask.jsonify({"error": "Некорректные данные для частичного обновления сущности"}), 400

        model = mapping_factory().to_model(dto)
        store.update_entity(k, id, model)
        cf = convert_factory()
        return flask.jsonify(cf.Convert(model)), 200
    except (operation_exception, arguments_exception) as ex:
        return flask.jsonify({"error": str(ex)}), 400
    except Exception as ex:
        return flask.jsonify({"error": f"Внутренняя ошибка: {ex}"}), 400


def delete_entity(entity_type: str, id: str):
    """DELETE /api/entities/{entity_type}/{id} — удалить сущность"""
    store = storage_manager()
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