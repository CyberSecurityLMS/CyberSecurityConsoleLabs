# Уязвимое приложение - лабораторная работа по повышению привилегий
# Студенту нужно исправить этот файл, добавив проверку прав доступа при обновлении профиля

import sys
import json

# Имитация базы данных пользователей
USERS = {
    "chris": {"password": "password789", "role": "user", "email": "chris@example.com"},
    "david": {"password": "passwordabc", "role": "admin", "email": "david@example.com"}
}

def update_profile_vulnerable(username, profile_data_json):
    """
    Уязвимая функция обновления профиля
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция позволяет изменять любые поля профиля, включая 'role'.
    Тебе нужно:
    1. Добавить проверку изменяемых полей
    2. Запретить изменение поля 'role' для обычных пользователей
    3. Разрешить изменение только безопасных полей (email)
    4. Возвращать ошибку при попытке изменить запрещенные поля
    
    После исправления тесты из test_privilege_escalation.py должны пройти успешно.
    """
    if username not in USERS:
        print(f"Ошибка: Пользователь {username} не найден.")
        return False

    try:
        profile_data = json.loads(profile_data_json)
        print(f"Обновление профиля для {username} данными: {profile_data}")

        # TODO: Добавьте проверку полей здесь
        for key, value in profile_data.items():
            if key in USERS[username]:
                USERS[username][key] = value
                print(f"  Установлено {key} = {value}")

        print(f"Профиль {username} обновлен: {USERS[username]}")
        return True

    except json.JSONDecodeError:
        print("Ошибка: Некорректный формат JSON данных профиля.")
        return False
    except Exception as e:
        print(f"Ошибка при обновлении профиля: {e}")
        return False

def login(username, password):
    """Функция аутентификации пользователя"""
    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Пользователь {username} вошел. Роль: {user['role']}")
        return True
    print("Неверное имя пользователя или пароль.")
    return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python vulnerable_app.py <username> <password> '<profile_json>'")
        print("Пример (безопасный): python vulnerable_app.py chris password789 '{\"email\": \"new@example.com\"}'")
        print("Пример (уязвимость): python vulnerable_app.py chris password789 '{\"role\": \"admin\"}'")
        sys.exit(1)

    user = sys.argv[1]
    pwd = sys.argv[2]
    profile_json = sys.argv[3]

    print("--- Попытка входа ---")
    if login(user, pwd):
        print("\n--- Попытка обновления профиля ---")
        update_profile_vulnerable(user, profile_json)

        print("\n--- Проверка роли после обновления ---")
        print(f"Текущая роль {user}: {USERS[user]['role']}")