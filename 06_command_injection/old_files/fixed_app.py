# 06_command_injection/fixed_app.py
import sys
import platform
import subprocess
# import shlex # Понадобится, если бы мы использовали shell=True

# Функция для проверки доступности хоста (ping) - БЕЗОПАСНАЯ ВЕРСИЯ
def safe_check_host(hostname):
    # Определяем команду и аргументы для текущей ОС
    system = platform.system().lower()
    if system == "windows":
        command_args = ["ping", "-n", "1", hostname]
    elif system in ["linux", "darwin"]: # darwin это macOS
        command_args = ["ping", "-c", "1", hostname]
    else:
        print(f"Неподдерживаемая ОС: {system}")
        return False

    # ИСПРАВЛЕНО: Используем subprocess.run с списком аргументов
    # shell=False (по умолчанию) - безопасно, оболочка не используется для парсинга команды.
    # Каждый элемент списка command_args передается как отдельный аргумент команде ping.
    print(f"Выполнение команды (безопасно): {command_args}")

    try:
        # capture_output=True перехватывает вывод команды (stdout/stderr)
        # text=True декодирует вывод в текст
        # timeout=5 устанавливает тайм-аут в 5 секунд
        result = subprocess.run(command_args, capture_output=True, text=True, check=False, timeout=5)

        print("-" * 20)
        print("STDOUT:")
        print(result.stdout if result.stdout else "[пусто]")
        print("STDERR:")
        print(result.stderr if result.stderr else "[пусто]")
        print(f"Код возврата: {result.returncode}")
        print("-" * 20)

        if result.returncode == 0:
            print(f"Хост '{hostname}' доступен.")
            return True
        else:
            # Код возврата может быть не 0 и для доступного хоста при проблемах (напр., TTL истек)
            # Но для простоты считаем любой ненулевой код ошибкой или недоступностью
            print(f"Хост '{hostname}' недоступен или произошла ошибка.")
            return False
    except subprocess.TimeoutExpired:
         print("Ошибка: Команда выполнялась слишком долго (timeout).")
         return False
    except FileNotFoundError:
         print("Ошибка: Команда 'ping' не найдена. Убедитесь, что она установлена и доступна в PATH.")
         return False
    except Exception as e:
        print(f"Непредвиденная ошибка при выполнении команды: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python fixed_app.py <hostname>")
        print("Пример (безопасный): python fixed_app.py google.com")
        print("Пример (НЕ СРАБОТАЕТ): python fixed_app.py \"google.com ; ls -la\"")
        sys.exit(1)

    user_input = sys.argv[1]
    print(f"Проверка хоста: {user_input}")
    safe_check_host(user_input) 