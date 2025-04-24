# 02_access_control/vulnerable_app.py
import sys

# Имитация базы данных пользователей и их ролей
USERS = {
    "alice": {"role": "admin", "password": "password123"},
    "bob": {"role": "user", "password": "password456"},
}

# Функция, которая должна быть доступна только админу
def delete_user(username_to_delete):
    # УЯЗВИМОСТЬ: Нет проверки роли текущего пользователя!
    # Любой аутентифицированный пользователь может удалить другого.
    if username_to_delete in USERS:
        del USERS[username_to_delete]
        print(f"Пользователь '{username_to_delete}' успешно удален.")
        print(f"Текущие пользователи: {list(USERS.keys())}")
    else:
        print(f"Ошибка: Пользователь '{username_to_delete}' не найден.")

# Простая имитация входа в систему
def login(username, password):
    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"Добро пожаловать, {username}! Ваша роль: {user['role']}")
        return user # Возвращаем информацию о пользователе (включая роль)
    else:
        print("Неверное имя пользователя или пароль.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python vulnerable_app.py <login_user> <login_password> <user_to_delete>")
        print("Пример (админ удаляет): python vulnerable_app.py alice password123 bob")
        print("Пример (ПОЛЬЗОВАТЕЛЬ удаляет - УЯЗВИМОСТЬ): python vulnerable_app.py bob password456 alice")
        sys.exit(1)

    login_user = sys.argv[1]
    login_pass = sys.argv[2]
    user_to_delete = sys.argv[3]

    current_user = login(login_user, login_pass)

    if current_user:
        print(f"\nПопытка удалить пользователя '{user_to_delete}' от имени '{login_user}'...")
        # Здесь происходит вызов опасной функции без проверки роли
        delete_user(user_to_delete)
    else:
        print("Вход не выполнен.") 