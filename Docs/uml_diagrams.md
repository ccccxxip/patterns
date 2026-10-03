## settings_manager

### Описание

`settings_manager` — менеджер настроек приложения, реализованный как **Singleton**. Отвечает за загрузку данных из JSON (`load()`) и их конвертацию (`convert()`) в типизированную модель `settings_model`, которая включает в себя реквизиты компании (`organization_model`). Все параметры защищены валидацией через `validator`.

```mermaid
classDiagram
    class abstract_manager {
        <<abstract>>
        #_file_name: str
        #_is_loaded: bool
        #_data: list
        +load(file_name: str) None
        +convert() bool
        +is_loaded: bool
    }

    class base_model {
        <<abstract>>
        #_id: str
        #_name: str
        +id: str
        +name: str
    }

    class settings_manager {
        <<Singleton>>
        -__default_file_name: str$
        -__settings: settings_model
        -__data: dict
        +__new__(cls) settings_manager$
        +__init__() None
        +load(file_name: str) None
        +convert() bool
        +settings: settings_model
    }

    class settings_model {
        -__organization: organization_model
        -__boss_name: str
        -__account_name: str
        -__is_first_start: bool
        +organization: organization_model
        +boss_name: str
        +account_name: str
        +is_first_start: bool
    }

    class organization_model {
        +inn: str
        +bik: str
        +account: str
        +ownership_form: str
    }

    class validator {
        <<utility>>
        +validate(value, type_, len_, field_name) bool$
    }

    class operation_exception {
        <<exception>>
    }


    abstract_manager <|-- settings_manager : наследование
    base_model <|-- settings_model : наследование
    base_model <|-- organization_model : наследование

    settings_manager *-- settings_model : создаёт и хранит
    settings_model o-- organization_model : агрегирует реквизиты

    settings_manager ..> validator : использует
    settings_manager ..> operation_exception : выбрасывает
    settings_model ..> validator : использует
```

## storage_manager

### Описание

`storage_manager` — менеджер хранилища данных, реализованный как **Singleton**. Отвечает за хранение и управление доменными сущностями в памяти (`__data`), обеспечение уникальности записей через метод `add()` (который также использует `validator` для проверки ключа справочника), а также за автоматическую генерацию базовых справочников при первом запуске приложения (проверяя флаг `is_first_start`, который хранится в `settings_model`, получаемом через `settings_manager`).

Все доменные модели (`unit_model`, `warehouse_model`, `nomenclature_model`, `nomenclature_group_model`) наследуются от общего абстрактного класса `base_model`.

```mermaid
classDiagram
    class abstract_manager {
        <<abstract>>
        #_file_name: str
        #_is_loaded: bool
        #_data: list
        +load(file_name: str) None
        +convert() bool
        +is_loaded: bool
    }
    
    class base_model {
        <<abstract>>
        #_id: str
        #_name: str
        +id: str
        +name: str
    }

    class storage_manager {
        <<Singleton>>
        -__data: dict
        +__new__(cls) storage_manager$
        +load(file_name: str) None
        +convert() bool
        +add(key: str, item) None
        +data: dict
        +warehouses: list
        +units: list
        +groups: list
        +nomenclatures: list
    }

    class nomenclature_model {
        -__full_name: str
        -__group: nomenclature_group_model
        -__unit: unit_model
        +full_name: str
        +group: nomenclature_group_model
        +unit: unit_model
    }
    
    class nomenclature_group_model {
        <<model>>
    }
    
    class unit_model {
        -__ratio: float
        -__base_unit: unit_model
        +ratio: float
        +base_unit: unit_model
        +to_base(quantity: float) float
    }
    
    class warehouse_model {
        -__address: str
        +address: str
    }

    class settings_manager {
        +settings: settings_model
    }
    class settings_model {
        +is_first_start: bool
    }
    class validator {
        <<utility>>
        +validate(value, type_, len_, field_name) bool$
    }


    abstract_manager <|-- storage_manager
    base_model <|-- unit_model
    base_model <|-- warehouse_model
    base_model <|-- nomenclature_group_model
    base_model <|-- nomenclature_model

    storage_manager o-- unit_model : хранит
    storage_manager o-- warehouse_model : хранит
    storage_manager o-- nomenclature_group_model : хранит
    storage_manager o-- nomenclature_model : хранит

    nomenclature_model --> nomenclature_group_model : ссылается
    nomenclature_model --> unit_model : ссылается
    unit_model --> unit_model : базовая ед.

    storage_manager --> settings_manager : запрашивает
    settings_manager --> settings_model : содержит
    storage_manager ..> settings_model : проверяет флаг
    storage_manager ..> validator : валидирует
```