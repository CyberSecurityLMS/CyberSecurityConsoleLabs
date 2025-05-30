# Уязвимое приложение - лабораторная работа по контролю доступа
# Студенту нужно исправить этот файл, добавив проверку роли пользователя

import sys

# Имитация базы данных пользователей и их ролей
USERS = {
    "alice": {"role": "admin", "password": "password123"},
    "bob": {"role": "user", "password": "password456"},
}

def delete_user(username_to_delete):
    """
    Уязвимая функция удаления пользователя.
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция не проверяет права доступа вызывающего пользователя.
    Тебе нужно:
    1. Добавить параметр caller_role (роль вызывающего)
    2. Добавить проверку, что caller_role == "admin"
    3. Возвращать ошибку, если права недостаточны
    
    После исправления тесты из test_access_control.py должны пройти успешно.
    """
    # TODO: Добавьте проверку прав доступа здесь
    if username_to_delete in USERS:
        del USERS[username_to_delete]
        print(f"Пользователь '{username_to_delete}' успешно удален.")
        print(f"Текущие пользователи: {list(USERS.keys())}")
    else:
        print(f"Ошибка: Пользователь '{username_to_delete}' не найден.")

def login(username, password):
    """Функция аутентификации пользователя"""
    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Добро пожаловать, {username}! Ваша роль: {user['role']}")
        return user
    else:
        print("Неверное имя пользователя или пароль.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python vulnerable_app.py <login_user> <login_password> <user_to_delete>")
        print("Пример уязвимости (пользователь удаляет админа): python vulnerable_app.py bob password456 alice")
        sys.exit(1)

    login_user = sys.argv[1]
    login_pass = sys.argv[2]
    user_to_delete = sys.argv[3]

    current_user = login(login_user, login_pass)

    if current_user:
        print(f"\nПопытка удалить пользователя '{user_to_delete}' от имени '{login_user}'...")
        # Уязвимый вызов - нет передачи роли пользователя
        delete_user(user_to_delete)
    else:
        print("Вход не выполнен.")