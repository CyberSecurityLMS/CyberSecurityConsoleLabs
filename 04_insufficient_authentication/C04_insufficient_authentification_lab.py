# Уязвимое приложение - лабораторная работа по недостаточной аутентификации
# Студенту нужно исправить этот файл, добавив проверку аутентификации

import sys

# Имитация базы данных пользователей
USERS = {
    "1": {"username": "admin", "password": "admin_pass", "secret": "Admin's Secret Data"},
    "2": {"username": "guest", "password": "guest_pass", "secret": "Guest's Personal Info"}
}

def login(user_id, password):
    """Функция входа в систему"""
    user = USERS.get(user_id)
    if user and user["password"] == password:
        print(f"Пользователь {user['username']} ({user_id}) успешно вошел.")
        return user
    else:
        print("Неверный ID пользователя или пароль.")
        return None

def get_user_profile(user_id):
    """
    Уязвимая функция просмотра профиля
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция позволяет просматривать профиль без аутентификации.
    Тебе нужно:
    1. Добавить проверку текущего пользователя (через сессию или глобальную переменную)
    2. Разрешить просматривать только свой профиль
    3. Возвращать ошибку, если пользователь не аутентифицирован
    
    После исправления тесты из test_authentication.py должны пройти успешно.
    """
    # TODO: Добавьте проверку аутентификации здесь
    user = USERS.get(user_id)
    if user:
        print(f"\n--- Профиль пользователя ID {user_id} ---")
        print(f"  Имя пользователя: {user['username']}")
        print(f"  Секретная информация: {user['secret']}")
        print("------------------------------------")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

if __name__ == "__main__":
    print("Доступные действия:")
    print("1. login <user_id> <password> - Войти в систему")
    print("2. profile <user_id> - Показать профиль (УЯЗВИМОСТЬ!)")
    print("\nПример эксплуатации уязвимости:")
    print("python vulnerable_app.py profile 1 - просмотр профиля админа без входа")

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
        login(user_id, password)

    elif action == "profile":
        if len(sys.argv) != 3:
            print("Использование: python vulnerable_app.py profile <user_id>")
            sys.exit(1)
        user_id = sys.argv[2]
        get_user_profile(user_id)

    else:
        print(f"Неизвестное действие: {action}")