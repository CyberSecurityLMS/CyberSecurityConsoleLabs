# Уязвимое приложение - лабораторная работа по внедрению кода
# Студенту нужно исправить этот файл, заменив опасный eval() на безопасную альтернативу

import sys

def calculate(expression):
    """
    Уязвимая функция вычисления математических выражений
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция использует опасную функцию eval(), которая выполняет любой код Python.
    Тебе нужно:
    1. Заменить eval() на безопасный парсер математических выражений
    2. Реализовать проверку, что выражение содержит только разрешенные операции
    3. Запретить выполнение любых вызовов функций и обращений к переменным
    
    После исправления тесты из test_code_injection.py должны пройти успешно.
    """
    try:
        # TODO: ЗАМЕНИТЕ ЭТУ СТРОКУ НА БЕЗОПАСНУЮ РЕАЛИЗАЦИЮ
        result = eval(expression)
        print(f"Результат выражения '{expression}': {result}")
        return result
    except Exception as e:
        print(f"Ошибка вычисления выражения '{expression}': {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py \"<выражение>\"")
        print("Пример (безопасный): python vulnerable_app.py \"2 + 2 * 3\"")
        print("Пример (уязвимость): python vulnerable_app.py \"__import__('os').system('echo HACKED')\"")
        sys.exit(1)

    user_input = sys.argv[1]
    print(f"Получено выражение/код: {user_input}")
    calculate(user_input)