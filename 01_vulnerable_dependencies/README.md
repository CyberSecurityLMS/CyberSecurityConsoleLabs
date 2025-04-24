# Уязвимость 1: Уязвимые Зависимости (Vulnerable Dependencies)

Это задание демонстрирует, как использование устаревшей или известной уязвимой библиотеки (`PyYAML < 5.1`) может привести к выполнению произвольного кода.

## Файлы

*   `vulnerable_app.py`: Уязвимое приложение, использующее `yaml.load()`.
*   `fixed_app.py`: Исправленное приложение, использующее `yaml.safe_load()`.
*   `requirements.txt`: Указывает на уязвимую версию `PyYAML==3.13`.
*   `malicious_config.yaml`: Пример YAML-файла для эксплуатации уязвимости (создается автоматически при запуске `vulnerable_app.py` без аргументов).

## Описание уязвимости

Библиотека `PyYAML` в версиях до 5.1 имеет опасную функцию `yaml.load()`. При обработке специально созданного YAML-файла эта функция может десериализовать не только данные, но и выполнять произвольные объекты Python, что приводит к выполнению кода (Code Execution).

В `vulnerable_app.py` используется именно эта функция:
```python
data = yaml.load(f, Loader=yaml.Loader)
```

## Эксплуатация

1.  **Установите уязвимую зависимость:**
    ```bash
    # Убедитесь, что вы в папке 01_vulnerable_dependencies или указываете полный путь
    # Возможно, потребуется создать виртуальное окружение:
    # python -m venv venv
    # source venv/bin/activate  # (Linux/macOS)
    # .\venv\Scripts\activate  # (Windows)
    pip install -r requirements.txt
    ```
2.  **Запустите уязвимое приложение без аргументов**, чтобы создать `malicious_config.yaml`:
    ```bash
    python vulnerable_app.py
    ```
    Содержимое `malicious_config.yaml`:
    ```yaml
    !!python/object/apply:builtins.print
    args: ["Vulnerability Exploited! Привет из YAML!"]
    ```
    Этот YAML использует тег `!!python/object/apply` для вызова функции `print` из модуля `builtins`.
3.  **Запустите уязвимое приложение с вредоносным файлом:**
    ```bash
    python vulnerable_app.py malicious_config.yaml
    ```
    Вы увидите, что строка "Vulnerability Exploited! Привет из YAML!" будет напечатана, что подтверждает выполнение кода, заданного в YAML.

## Исправление

Уязвимость устраняется двумя способами:

1.  **Использование безопасной функции:** Вместо `yaml.load()` следует всегда использовать `yaml.safe_load()`, если вы не уверены в источнике YAML-данных. `safe_load` обрабатывает только стандартные теги YAML и не выполняет код. Это сделано в `fixed_app.py`:
    ```python
    data = yaml.safe_load(f)
    ```
2.  **Обновление зависимости:** Необходимо обновить `PyYAML` до безопасной версии (>= 5.1). В современных версиях `yaml.load()` требует явного указания `Loader`, и использование `yaml.FullLoader` (который все еще может быть опасен) вызывает предупреждение. Рекомендуется всегда использовать `safe_load`.

## Проверка исправления

1.  **Установите безопасную версию (необязательно, т.к. `fixed_app.py` использует `safe_load`):**
    ```bash
    pip install "PyYAML>=5.1"
    ```
2.  **Запустите исправленное приложение с тем же вредоносным файлом:**
    ```bash
    python fixed_app.py malicious_config.yaml
    ```
    Вы увидите ошибку парсинга YAML (`could not determine a constructor for the tag 'tag:yaml.org,2002:python/object/apply'`) или просто загруженные данные без выполнения кода. Это показывает, что `safe_load` предотвратил атаку. 