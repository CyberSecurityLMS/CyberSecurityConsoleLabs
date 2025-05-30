# Уязвимое приложение - лабораторная работа по инъекции команд
# Студенту нужно исправить этот файл, заменив опасный os.system() на безопасную альтернативу

import os
import sys
import platform

def check_host(hostname):
    """
    Уязвимая функция проверки доступности хоста
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция использует опасный os.system() с конкатенацией строк.
    Тебе нужно:
    1. Заменить os.system() на subprocess.run()
    2. Передавать команду и аргументы в виде списка
    3. Убедиться, что shell=False (по умолчанию)
    4. Обрабатывать возможные ошибки выполнения
    
    После исправления тесты из test_command_injection.py должны пройти успешно.
    """
    # Определяем команду ping для текущей ОС
    if platform.system().lower() == "windows":
        base_command = "ping -n 1 "
    else:
        base_command = "ping -c 1 "

    # TODO: ЗАМЕНИТЕ ЭТУ СТРОКУ НА БЕЗОПАСНУЮ РЕАЛИЗАЦИЮ
    command = base_command + hostname
    print(f"Выполнение команды: {command}")

    try:
        exit_code = os.system(command)
        print("-" * 20)
        if exit_code == 0:
            print(f"Хост '{hostname}' доступен.")
        else:
            print(f"Хост '{hostname}' недоступен (код: {exit_code}).")
        return exit_code == 0
    except Exception as e:
        print(f"Ошибка при выполнении команды: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py <hostname>")
        print("Пример (безопасный): python vulnerable_app.py google.com")
        print("Пример (уязвимость): python vulnerable_app.py \"google.com ; ls -la\"")
        sys.exit(1)

    user_input = sys.argv[1]
    print(f"Проверка хоста: {user_input}")
    check_host(user_input)