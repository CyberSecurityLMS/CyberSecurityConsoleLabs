# 04_insufficient_authentication/fixed_app.py
import sys
import os # для файла сессии

# Имитация базы данных пользователей
USERS = {
    "1": {"username": "admin", "password": "admin_pass", "secret": "Admin's Secret Data"},
    "2": {"username": "guest", "password": "guest_pass", "secret": "Guest's Personal Info"}
}

# Хранение состояния входа (будет загружаться/сохраняться в файл)
current_logged_in_user_id = None
session_file = ".user_session.tmp" # Скрытый временный файл

# Функция для загрузки состояния сессии
def load_session():
    global current_logged_in_user_id
    if os.path.exists(session_file):
        try:
            with open(session_file, "r") as f:
                user_id = f.read().strip()
                if user_id in USERS: # Проверяем, валиден ли ID из сессии
                    current_logged_in_user_id = user_id
                else:
                    current_logged_in_user_id = None
                    os.remove(session_file) # Удаляем невалидную сессию
        except Exception:
             current_logged_in_user_id = None
    else:
        current_logged_in_user_id = None

# Функция для сохранения состояния сессии
def save_session():
    try:
        with open(session_file, "w") as f:
            f.write(current_logged_in_user_id if current_logged_in_user_id else "")
    except Exception as e:
        print(f"Предупреждение: не удалось сохранить состояние сессии ({e})")

# Функция для входа
def login(user_id, password):
    global current_logged_in_user_id
    user = USERS.get(user_id)
    if user and user["password"] == password:
        print(f"Пользователь {user['username']} ({user_id}) успешно вошел.")
        current_logged_in_user_id = user_id # Запоминаем ID вошедшего пользователя
        return True
    else:
        print("Неверный ID пользователя или пароль.")
        current_logged_in_user_id = None
        return False

# Функция для выхода
def logout():
    global current_logged_in_user_id
    load_session() # Загружаем сессию перед выходом
    if current_logged_in_user_id:
        print(f"Пользователь {USERS[current_logged_in_user_id]['username']} вышел.")
        current_logged_in_user_id = None
    else:
        print("Никто не вошел в систему.")

# Функция для получения профиля ТЕКУЩЕГО пользователя
def get_my_profile():
    load_session() # Убедимся, что сессия загружена
    # ИСПРАВЛЕНО: Требуется аутентификация
    if not current_logged_in_user_id:
        print("Ошибка: Вы должны войти в систему, чтобы просмотреть свой профиль.")
        print("Используйте: login <user_id> <password>")
        return

    # ИСПРАВЛЕНО: Пользователь видит только свой профиль
    user = USERS.get(current_logged_in_user_id)
    if user:
        print(f"\n--- Ваш профиль (Пользователь ID {current_logged_in_user_id}) ---")
        print(f"  Имя пользователя: {user['username']}")
        print(f"  Секретная информация: {user['secret']}")
        print("------------------------------------")
    # Эта ветка else не должна сработать, если логика login верна
    else:
         print("Внутренняя ошибка: не найден профиль для вошедшего пользователя.")

if __name__ == "__main__":
    load_session() # Загружаем сессию при старте

    print("Доступные действия:")
    print("1. login <user_id> <password> - Войти в систему")
    print("2. profile                 - Показать свой профиль (требуется вход)")
    print("3. logout                  - Выйти из системы")
    print("Текущий пользователь (из сессии):", current_logged_in_user_id if current_logged_in_user_id else "Никто")
    print("Пример: ")
    print("   python fixed_app.py login 1 admin_pass")
    print("   python fixed_app.py profile")
    print("   python fixed_app.py logout")

    if len(sys.argv) < 2:
        print("\nОшибка: Не указано действие.")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "login":
        if len(sys.argv) != 4:
            print("Использование: python fixed_app.py login <user_id> <password>")
            sys.exit(1)
        user_id = sys.argv[2]
        password = sys.argv[3]
        login(user_id, password)

    elif action == "profile":
        # Исправленный вызов - проверяет логин внутри функции
        get_my_profile()

    elif action == "logout":
        logout()

    else:
        print(f"Неизвестное действие: {action}")

    # Сохраняем состояние сессии после выполнения действия
    save_session() 