# 05_code_injection/vulnerable_app.py
import sys

# Простой калькулятор, использующий eval для вычисления выражения
def calculate(expression):
    try:
        # УЯЗВИМОСТЬ: eval() выполняет любую строку как код Python!
        result = eval(expression)
        print(f"Результат выражения '{expression}': {result}")
        return result
    except Exception as e:
        print(f"Ошибка вычисления выражения '{expression}': {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py \"<математическое_выражение_или_КОД>\"")
        print("Пример (безопасный): python vulnerable_app.py \"2 + 2 * 3\"")
        print("Пример (УЯЗВИМЫЙ): python vulnerable_app.py \"__import__('os').system('echo HACKED by Code Injection!')\"")
        # Для Windows может понадобиться:
        # print("Пример (УЯЗВИМЫЙ Windows): python vulnerable_app.py \"__import__('os').system('dir')\"")
        sys.exit(1)

    user_input = sys.argv[1]
    print(f"Получено выражение/код: {user_input}")
    calculate(user_input) 