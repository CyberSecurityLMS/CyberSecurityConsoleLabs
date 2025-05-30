# 08_privilege_escalation/vulnerable_app.py
import sys
import json # Для имитации сохранения/загрузки данных профиля

# Имитация базы данных пользователей
USERS = {
    "chris": {"password": "password789", "role": "user", "email": "chris@example.com"},
    "david": {"password": "passwordabc", "role": "admin", "email": "david@example.com"}
}

# Уязвимая функция обновления профиля
def update_profile_vulnerable(username, profile_data_json):
    """Обновляет данные профиля пользователя.
       УЯЗВИМОСТЬ: Позволяет пользователю изменить любое поле, включая 'role'.
    """
    if username not in USERS:
        print(f"Ошибка: Пользователь {username} не найден.")
        return False

    try:
        # Загружаем JSON данные от пользователя
        profile_data = json.loads(profile_data_json)

        # ПРОВЕРКИ НЕТ: Просто обновляем все поля из полученного JSON
        print(f"Обновление профиля для {username} данными: {profile_data}")
        for key, value in profile_data.items():
            if key in USERS[username]: # Обновляем только существующие ключи (слабая защита)
                 # УЯЗВИМОСТЬ ЗДЕСЬ: Позволяет обновить и 'role'
                 USERS[username][key] = value
                 print(f"  Установлено {key} = {value}")
            # Игнорируем попытки добавить новые ключи типа 'is_super_admin'
            # Но не мешаем изменить 'role' на 'admin'

        print(f"Профиль {username} обновлен: {USERS[username]}")
        return True

    except json.JSONDecodeError:
        print("Ошибка: Некорректный формат JSON данных профиля.")
        return False
    except Exception as e:
        print(f"Ошибка при обновлении профиля: {e}")
        return False

# Простая имитация входа
def login(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Пользователь {username} вошел. Роль: {user['role']}")
        return True
    print("Неверное имя пользователя или пароль.")
    return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python vulnerable_app.py <username> <password> '<profile_json_data>'")
        print("Пример (смена email): python vulnerable_app.py chris password789 '{\"email\": \"new.chris@example.com\"}'")
        print("Пример (УЯЗВИМЫЙ - повышение роли): python vulnerable_app.py chris password789 '{\"role\": \"admin\", \"email\": \"pwned@example.com\"}'")
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
    else:
        print("Вход не удался. Обновление профиля невозможно.") 