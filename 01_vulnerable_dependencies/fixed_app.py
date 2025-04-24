# 01_vulnerable_dependencies/fixed_app.py
import yaml
import sys

# БЕЗОПАСНО: Использование yaml.safe_load()
# Эта функция загружает только простые YAML-теги и предотвращает выполнение кода.
def safe_load_config(filename):
    try:
        with open(filename, 'r') as f:
            # Безопасная функция
            data = yaml.safe_load(f)
            print("Конфигурация безопасно загружена:")
            print(data)
            return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    # PyYAML может выбросить специфичные ошибки парсинга
    except yaml.YAMLError as e:
        print(f"Ошибка при безопасной загрузке YAML: {e}")
        return None
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python fixed_app.py <имя_файла_config.yaml>")
        print("Попробуйте запустить с тем же 'malicious_config.yaml',")
        print("чтобы увидеть, как safe_load предотвращает выполнение кода.")
        sys.exit(1)

    config_file = sys.argv[1]
    safe_load_config(config_file) 