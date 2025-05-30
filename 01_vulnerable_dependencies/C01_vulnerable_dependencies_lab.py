# Уязвимое приложение - лабораторная работа по уязвимым зависимостям
# Студенту нужно исправить этот файл, заменив yaml.load() на безопасную альтернативу

import pyyaml
import sys
import os

def load_config(filename):
    """
    Уязвимая функция загрузки конфигурации из YAML-файла.
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция использует опасный метод yaml.load(), который может выполнять произвольный код.
    Тебе нужно заменить его на безопасную альтернативу - yaml.safe_load().
    
    После исправления тесты из test_vulnerable_app.py должны пройти успешно.
    """
    try:
        with open(filename, 'r') as f:
            # TODO: ЗАМЕНИТЕ ЭТУ СТРОКУ НА БЕЗОПАСНУЮ ВЕРСИЮ
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
        print("Создаем пример вредоносного YAML файла для демонстрации уязвимости...")
        
        malicious_yaml = """!!python/object/apply:builtins.print
args: ["Vulnerability Exploited! Привет из YAML!"]
"""
        try:
            with open("malicious_config.yaml", "w") as f:
                f.write(malicious_yaml)
            print("Создан пример вредоносного YAML файла: malicious_config.yaml")
            print("Попробуйте запустить: python vulnerable_app.py malicious_config.yaml")
            print("После исправления кода этот файл не должен выполнять код при загрузке.")
        except Exception as e:
            print(f"Не удалось создать пример файла: {e}")
        sys.exit(1)

    config_file = sys.argv[1]
    load_config(config_file)