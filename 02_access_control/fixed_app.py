# 02_access_control/fixed_app.py
import sys

# Имитация базы данных пользователей и их ролей
USERS = {
    "alice": {"role": "admin", "password": "password123"},
    "bob": {"role": "user", "password": "password456"},
}

# Функция, которая должна быть доступна только админу
def delete_user(caller_role, username_to_delete):
    # ИСПРАВЛЕНО: Добавлена проверка роли текущего пользователя
    if caller_role != "admin":
        print("Ошибка доступа: Только администраторы могут удалять пользователей.")
        return

    if username_to_delete in USERS:
        # Не позволяем админу удалить самого себя в этом примере
        if username_to_delete == "alice" and caller_role == "admin": # Пример самозащиты
             print("Администратор не может удалить самого себя.")
             return
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
        return user
    else:
        print("Неверное имя пользователя или пароль.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python fixed_app.py <login_user> <login_password> <user_to_delete>")
        print("Пример (админ удаляет): python fixed_app.py alice password123 bob")
        print("Пример (пользователь ПЫТАЕТСЯ удалить - БЕЗОПАСНО): python fixed_app.py bob password456 alice")
        sys.exit(1)

    login_user_name = sys.argv[1]
    login_pass = sys.argv[2]
    user_to_delete = sys.argv[3]

    current_user_data = login(login_user_name, login_pass)

    if current_user_data:
        print(f"\nПопытка удалить пользователя '{user_to_delete}' от имени '{login_user_name}'...")
        # Передаем роль текущего пользователя для проверки прав
        delete_user(current_user_data['role'], user_to_delete)
    else:
        print("Вход не выполнен.") 