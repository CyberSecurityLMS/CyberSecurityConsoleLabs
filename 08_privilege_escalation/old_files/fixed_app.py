# 08_privilege_escalation/fixed_app.py
import sys
import json
import copy # Для глубокой копии

# Имитация базы данных пользователей (исходное состояние)
INITIAL_USERS_STATE = {
    "chris": {"password": "password789", "role": "user", "email": "chris@example.com"},
    "david": {"password": "passwordabc", "role": "admin", "email": "david@example.com"}
}

# Рабочая копия данных, которую будем изменять
current_users_state = {}

# Безопасная функция обновления профиля
def update_profile_secure(username, profile_data_json, users_db):
    """Обновляет данные профиля пользователя в переданном словаре users_db.
       ИСПРАВЛЕНО: Запрещает изменение поля 'role'.
    """
    if username not in users_db:
        print(f"Ошибка: Пользователь {username} не найден.")
        return False

    try:
        profile_data = json.loads(profile_data_json)

        print(f"Обновление профиля для {username} данными: {profile_data}")
        updated_fields = []
        forbidden_fields_attempted = []

        for key, value in profile_data.items():
            # ИСПРАВЛЕНО: Явно запрещаем изменение 'role' и 'password' через этот метод
            if key == "role":
                forbidden_fields_attempted.append(key)
                continue # Пропускаем обновление роли
            if key == "password": # Пароль тоже нельзя менять этим методом
                 forbidden_fields_attempted.append(key)
                 continue

            # Обновляем только другие существующие и разрешенные поля в users_db
            if key in users_db[username]:
                 users_db[username][key] = value # Изменяем переданный словарь
                 print(f"  Установлено {key} = {value}")
                 updated_fields.append(key)
            else:
                print(f"  Поле '{key}' не существует или не разрешено для обновления, проигнорировано.")

        if forbidden_fields_attempted:
            print(f"Предупреждение: Попытка изменить запрещенные поля ({', '.join(forbidden_fields_attempted)}) была проигнорирована.")

        if updated_fields:
            print(f"Профиль {username} обновлен: {users_db[username]}")
        else:
            if forbidden_fields_attempted:
                 print("Никаких допустимых изменений не применено.")
            else:
                 print("Никаких допустимых полей для обновления не найдено.")

        return True

    except json.JSONDecodeError:
        print("Ошибка: Некорректный формат JSON данных профиля.")
        return False
    except Exception as e:
        print(f"Ошибка при обновлении профиля: {e}")
        return False

# Простая имитация входа (использует текущее состояние)
def login(username, password, users_db):
    user_data = users_db.get(username)
    if user_data and user_data["password"] == password:
        print(f"Пользователь {username} вошел. Роль: {user_data['role']}")
        return True
    print("Неверное имя пользователя или пароль.")
    return False


if __name__ == "__main__":
    # Создаем рабочую копию состояния для этого запуска
    current_users_state = copy.deepcopy(INITIAL_USERS_STATE)

    if len(sys.argv) != 4:
        print("Использование: python fixed_app.py <username> <password> '<profile_json_data>'")
        print("Пример (смена email): python fixed_app.py chris password789 '{\"email\": \"new.chris@example.com\"}'")
        print("Пример (попытка повышения роли - БЕЗОПАСНО): python fixed_app.py chris password789 '{\"role\": \"admin\", \"email\": \"hacker@example.com\"}'")
        sys.exit(1)

    user = sys.argv[1]
    pwd = sys.argv[2]
    profile_json = sys.argv[3]

    # Запоминаем исходную роль из копии
    original_role = current_users_state.get(user, {}).get('role') if current_users_state.get(user) else None

    print("--- Попытка входа ---")
    # Логинимся используя текущее состояние
    if login(user, pwd, current_users_state):
        print("\n--- Попытка обновления профиля ---")
        # Обновляем текущее состояние
        update_successful = update_profile_secure(user, profile_json, current_users_state)

        print("\n--- Проверка роли после обновления ---")
        # Проверяем роль в измененном текущем состоянии
        current_role = current_users_state.get(user, {}).get('role')
        print(f"Текущая роль {user}: {current_role}")

        if original_role is not None and current_role != original_role:
             # Эта ветка не должна выполниться в исправленной версии
             print(f"!!! ОШИБКА ЛОГИКИ ИСПРАВЛЕНИЯ: Роль пользователя {user} изменилась с '{original_role}' на '{current_role}'! !!!")
        elif current_role == original_role and original_role is not None:
             print("Роль пользователя не изменилась (как и ожидалось).")
        else:
             print("Не удалось сравнить роли.") # Если пользователя не было изначально

    else:
        print("Вход не удался. Обновление профиля невозможно.") 