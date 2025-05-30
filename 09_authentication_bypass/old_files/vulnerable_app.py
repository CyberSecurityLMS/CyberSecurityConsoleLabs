# 09_authentication_bypass/vulnerable_app.py
import sys

# Имитация базы данных пользователей
USERS = {
    "root": {"password": "root_password", "data": "Super sensitive data"},
    "guest": {"password": "guest_password", "data": "Public info"}
}

# Уязвимая функция входа
def login_vulnerable(username, password):
    """Пытается аутентифицировать пользователя.
    УЯЗВИМОСТЬ: Неправильная обработка случая, когда пользователь не найден.
    Вместо возврата явного признака неудачи (напр., None или False),
    возвращается пустой словарь {}, который при нестрогой проверке
    может быть интерпретирован как успех.
    """
    print(f"Попытка входа для: {username}")
    user_data = USERS.get(username)

    if user_data:
        if user_data['password'] == password:
            print(f"Успешный вход для {username}.")
            return user_data # Возвращаем данные пользователя
        else:
            print("Неверный пароль.")
            return None # Явная неудача при неверном пароле
    else:
        print(f"Пользователь '{username}' не найден...")
        # УЯЗВИМОСТЬ: Возвращаем пустой словарь вместо None/False
        print("...возвращаем {} для имитации обхода аутентификации!")
        return {}


# Функция, требующая аутентификации
def access_sensitive_data(logged_in_user_data):
    """Пытается получить доступ к данным, проверяя результат логина.
    УЯЗВИМОСТЬ в проверке: 'if logged_in_user_data:' истинно для {},
    хотя {} не содержит реальных данных пользователя.
    """
    print(f"\nПроверка результата аутентификации: {logged_in_user_data}")
    if logged_in_user_data: # Эта проверка истинна и для {}, и для {'password':...}
        print("Проверка 'if logged_in_user_data' пройдена (результат не False/None).")
        # Попытка получить данные. Для {} .get вернет значение по умолчанию.
        secret = logged_in_user_data.get('data', '[ДАННЫЕ НЕ ПОЛУЧЕНЫ, НО ДОСТУП РАЗРЕШЕН!]')
        print("--- Доступ к 'защищенной' области разрешен ---")
        print(f"  Секретные данные: {secret}")
        print("-------------------------------------------")
    else: # Сюда попадем только если login_vulnerable вернул None (неверный пароль)
        print("Проверка 'if logged_in_user_data' НЕ пройдена.")
        print("Доступ запрещен.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nИспользование: python vulnerable_app.py <username> <password>")
        print("Пример (успешный вход): python vulnerable_app.py root root_password")
        print("Пример (неверный пароль): python vulnerable_app.py root wrongpass")
        print("Пример (ОБХОД - несуществующий юзер): python vulnerable_app.py non_existent_user anypassword")
        sys.exit(1)

    uname = sys.argv[1]
    pword = sys.argv[2]

    print("--- Вызов уязвимой функции входа ---")
    auth_result = login_vulnerable(uname, pword)

    print("\n--- Попытка доступа к данным после входа ---")
    access_sensitive_data(auth_result) 