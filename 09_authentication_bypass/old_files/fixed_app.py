# 09_authentication_bypass/fixed_app.py
import sys

# Имитация базы данных пользователей
USERS = {
    "root": {"password": "root_password", "data": "Super sensitive data"},
    "guest": {"password": "guest_password", "data": "Public info"}
}

# Исправленная функция входа
def login_secure(username, password):
    """Пытается аутентифицировать пользователя.
    ИСПРАВЛЕНО: Всегда возвращает None при любой ошибке аутентификации.
    """
    print(f"Попытка входа для: {username}")
    user_data = USERS.get(username)

    if not user_data:
        print(f"Пользователь '{username}' не найден.")
        return None # Явная неудача

    if user_data['password'] == password:
        print(f"Успешный вход для {username}.")
        return user_data # Возвращаем данные пользователя
    else:
        print("Неверный пароль.")
        return None # Явная неудача


# Исправленная функция, требующая аутентификации
def access_sensitive_data_secure(logged_in_user_data):
    """Пытается получить доступ к данным, строго проверяя результат логина."""
    print(f"\nПроверка результата аутентификации: {logged_in_user_data}")

    # ИСПРАВЛЕНО: Строгая проверка. Успешный вход - это словарь с данными, а не просто "что-то не None/False".
    # Проверяем, что это словарь и он не пустой (или содержит ожидаемый ключ, например 'data').
    if isinstance(logged_in_user_data, dict) and logged_in_user_data.get('data') is not None:
        print("Проверка аутентификации пройдена (получен валидный словарь пользователя).")
        secret = logged_in_user_data['data'] # Можно напрямую получить, т.к. проверили наличие
        print("--- Доступ к защищенным данным разрешен ---")
        print(f"  Секретные данные: {secret}")
        print("-----------------------------------------")
    else:
        print("Проверка аутентификации НЕ пройдена.")
        print("Доступ запрещен.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nИспользование: python fixed_app.py <username> <password>")
        print("Пример (успешный вход): python fixed_app.py root root_password")
        print("Пример (неверный пароль): python fixed_app.py root wrongpass")
        print("Пример (несуществующий юзер - БУДЕТ ОТКЛОНЕН): python fixed_app.py non_existent_user anypassword")
        sys.exit(1)

    uname = sys.argv[1]
    pword = sys.argv[2]

    print("--- Вызов безопасной функции входа ---")
    auth_result = login_secure(uname, pword)

    print("\n--- Попытка доступа к данным после входа ---")
    access_sensitive_data_secure(auth_result) 