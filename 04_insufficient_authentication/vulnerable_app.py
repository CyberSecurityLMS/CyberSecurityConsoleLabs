# 04_insufficient_authentication/vulnerable_app.py
import sys

# Имитация базы данных пользователей (пароли для логина, секреты для профиля)
USERS = {
    "1": {"username": "admin", "password": "admin_pass", "secret": "Admin's Secret Data"},
    "2": {"username": "guest", "password": "guest_pass", "secret": "Guest's Personal Info"}
}

# Функция для входа (для сравнения)
def login(user_id, password):
    user = USERS.get(user_id)
    if user and user["password"] == password:
        print(f"Пользователь {user['username']} ({user_id}) успешно вошел.")
        return user # Возвращаем данные пользователя при успехе
    else:
        print("Неверный ID пользователя или пароль.")
        return None

# Функция для получения профиля пользователя
def get_user_profile(user_id):
    # УЯЗВИМОСТЬ: Функция доступна без предварительной аутентификации!
    # Любой может запросить профиль любого пользователя, зная его ID.
    user = USERS.get(user_id)
    if user:
        print(f"\n--- Профиль пользователя ID {user_id} ---")
        print(f"  Имя пользователя: {user['username']}")
        print(f"  Секретная информация: {user['secret']}") # Показ чувствительных данных
        print("------------------------------------")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

if __name__ == "__main__":
    print("Доступные действия:")
    print("1. login <user_id> <password> - Войти в систему")
    print("2. profile <user_id> - Показать профиль пользователя (УЯЗВИМОСТЬ!)")
    print("Пример уязвимости: python vulnerable_app.py profile 1")

    if len(sys.argv) < 2:
        print("\nОшибка: Не указано действие.")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "login":
        if len(sys.argv) != 4:
            print("Использование: python vulnerable_app.py login <user_id> <password>")
            sys.exit(1)
        user_id = sys.argv[2]
        password = sys.argv[3]
        logged_in_user = login(user_id, password)
        if logged_in_user:
            print("Вход выполнен, но это действие не показывает профиль.")

    elif action == "profile":
        if len(sys.argv) != 3:
            print("Использование: python vulnerable_app.py profile <user_id>")
            sys.exit(1)
        user_id = sys.argv[2]
        # Уязвимый вызов - профиль показывается без проверки логина
        get_user_profile(user_id)

    else:
        print(f"Неизвестное действие: {action}") 