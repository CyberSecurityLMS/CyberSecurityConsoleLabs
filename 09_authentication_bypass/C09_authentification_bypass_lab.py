# Уязвимое приложение - лабораторная работа по обходу аутентификации
# Студенту нужно исправить этот файл, добавив строгие проверки аутентификации

import sys

# Имитация базы данных пользователей
USERS = {
    "admin": {"password": "secure123", "data": "Конфиденциальные данные администратора"},
    "user": {"password": "password456", "data": "Обычные данные пользователя"}
}

def login_vulnerable(username, password):
    """
    Уязвимая функция аутентификации
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция имеет две проблемы:
    1. Возвращает пустой словарь {} при несуществующем пользователе
    2. Недостаточно строго проверяет успешность аутентификации
    
    Тебе нужно:
    1. Всегда возвращать None при неудачной аутентификации
    2. Добавить строгую проверку наличия пользовательских данных
    
    После исправления тесты из test_auth_bypass.py должны пройти успешно.
    """
    print(f"Попытка входа для пользователя: {username}")
    user_data = USERS.get(username)

    if user_data:
        if user_data['password'] == password:
            print("Аутентификация успешна")
            return user_data
        else:
            print("Неверный пароль")
            return None
    else:
        print(f"Пользователь {username} не найден")
        # TODO: Исправьте эту строку - не возвращайте {}
        return {}  # Уязвимость: возвращаем пустой словарь вместо None

def access_restricted_data(auth_result):
    """
    Уязвимая функция доступа к данным
    
    ЗАДАНИЕ:
    Добавьте строгую проверку результата аутентификации:
    1. Проверяйте, что auth_result - это словарь
    2. Проверяйте наличие ключа 'data'
    3. Убедитесь, что данные не пустые
    """
    print("\nПопытка доступа к защищенным данным...")
    
    # TODO: Замените эту слабую проверку
    if auth_result:  # Эта проверка проходит для {}
        data = auth_result.get('data', 'Доступ получен, но данные отсутствуют!')
        print("Доступ разрешен!")
        print(f"Защищенные данные: {data}")
    else:
        print("Доступ запрещен: требуется аутентификация")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\nИспользование: python vulnerable_app.py <username> <password>")
        print("Пример (успешный вход): python vulnerable_app.py admin secure123")
        print("Пример (обход аутентификации): python vulnerable_app.py unknown anypass")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    print("\n=== Процесс аутентификации ===")
    auth_data = login_vulnerable(username, password)

    print("\n=== Попытка доступа к данным ===")
    access_restricted_data(auth_data)