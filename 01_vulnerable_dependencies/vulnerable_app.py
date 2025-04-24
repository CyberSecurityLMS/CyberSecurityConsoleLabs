# 01_vulnerable_dependencies/vulnerable_app.py
import yaml
import sys
import os # Import os for the example payload

# ОПАСНО: Использование yaml.load() с ненадежными данными
# В PyYAML < 5.1 yaml.load() может выполнять произвольный код.
def load_config(filename):
    try:
        with open(filename, 'r') as f:
            # Уязвимая функция
            data = yaml.load(f, Loader=yaml.Loader)
            print("Конфигурация загружена:")
            print(data)
            return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке YAML: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py <имя_файла_config.yaml>")
        # Создаем пример вредоносного файла для демонстрации
        # Используем безопасный способ демонстрации через print
        malicious_yaml = """!!python/object/apply:builtins.print
args: ["Vulnerability Exploited! Привет из YAML!"]
"""
        # Альтернативный опасный пример (создание файла): 
        # malicious_yaml = """!!python/object/apply:os.system\nargs: ['echo Vulnerability Exploited! > exploited.txt']\n"""
        try:
            with open("malicious_config.yaml", "w") as f:
                f.write(malicious_yaml)
            print("Создан пример вредоносного YAML файла: malicious_config.yaml")
            print("Попробуйте запустить: python 01_vulnerable_dependencies/vulnerable_app.py malicious_config.yaml")
        except Exception as e:
            print(f"Не удалось создать пример файла: {e}")
        sys.exit(1)

    config_file = sys.argv[1]
    load_config(config_file) 