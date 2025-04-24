# 06_command_injection/vulnerable_app.py
import os
import sys
import platform

# Функция для проверки доступности хоста (ping)
def check_host(hostname):
    # Определяем команду ping для текущей ОС
    if platform.system().lower() == "windows":
        # -n 1 - отправить только один пакет
        base_command = "ping -n 1 "
    else:
        # -c 1 - отправить только один пакет
        base_command = "ping -c 1 "

    # УЯЗВИМОСТЬ: Прямое добавление пользовательского ввода в команду ОС!
    # Символы вроде ';' или '&&' могут выполнить дополнительные команды.
    command = base_command + hostname
    print(f"Выполнение команды: {command}")

    try:
        # os.system() выполняет команду в системной оболочке
        exit_code = os.system(command)
        print("-" * 20)
        if exit_code == 0:
            print(f"Хост '{hostname}' доступен.")
        else:
            print(f"Хост '{hostname}' недоступен или произошла ошибка (код: {exit_code}).")
        return exit_code == 0
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py <hostname_или_КОМАНДА>")
        print("Пример (безопасный): python vulnerable_app.py google.com")
        # Примеры для Windows
        print("Пример (УЯЗВИМЫЙ Win): python vulnerable_app.py \"google.com & echo HACKED\"")
        print("Пример (УЯЗВИМЫЙ Win): python vulnerable_app.py \"google.com & dir\"")
        # Примеры для Linux/macOS
        print("Пример (УЯЗВИМЫЙ Lin/Mac): python vulnerable_app.py \"google.com ; echo HACKED\"")
        print("Пример (УЯЗВИМЫЙ Lin/Mac): python vulnerable_app.py \"google.com ; ls -la\"")
        sys.exit(1)

    user_input = sys.argv[1]
    print(f"Проверка хоста/выполнение: {user_input}")
    check_host(user_input) 