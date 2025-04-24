# 05_code_injection/fixed_app.py
import sys
import ast
import operator as op

# Ограниченный набор безопасных операторов
allowed_operators = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
    ast.USub: op.neg
}

# Ограниченный набор разрешенных имен (только числа)
allowed_names = {}

# Безопасная функция для вычисления простых математических выражений
def safe_eval_math(node):
    if isinstance(node, ast.Num): # <number> Python < 3.8
        return node.n
    elif isinstance(node, ast.Constant): # <number>, <string>, <bool>, None Python >= 3.8
        # Разрешаем только числа
        if isinstance(node.value, (int, float)):
            return node.value
        else:
            raise TypeError(f"Константа типа {type(node.value).__name__} не разрешена")
    elif isinstance(node, ast.Name): # <variable>
        # Разрешаем только если имя было ранее разрешено (здесь - нет)
        if node.id in allowed_names:
            return allowed_names[node.id]
        else:
            raise TypeError(f"Использование имени '{node.id}' не разрешено")
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        left = safe_eval_math(node.left)
        right = safe_eval_math(node.right)
        if type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](left, right)
        else:
             raise TypeError(f"Оператор {type(node.op).__name__} не разрешен")
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        operand = safe_eval_math(node.operand)
        if type(node.op) in allowed_operators:
             return allowed_operators[type(node.op)](operand)
        else:
            raise TypeError(f"Унарный оператор {type(node.op).__name__} не разрешен")
    else:
        # Проверяем, если это корень выражения (Expression node)
        if isinstance(node, ast.Expression):
            return safe_eval_math(node.body)
        raise TypeError(f"Узел типа {type(node).__name__} не разрешен")

# Функция-обертка для безопасного вычисления строки
def safe_calculate(expression):
    try:
        # 1. Парсим строку в абстрактное синтаксическое дерево (AST)
        # Используем Expression для одиночных выражений
        node = ast.parse(expression, mode='eval') 
        
        # 2. Вызываем нашу безопасную рекурсивную функцию для вычисления AST
        result = safe_eval_math(node) # Передаем сам Expression node
        print(f"Результат выражения '{expression}': {result}")
        return result

    except (SyntaxError, TypeError, RecursionError, Exception) as e:
        print(f"Ошибка безопасного вычисления выражения '{expression}': {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python fixed_app.py \"<математическое_выражение>\"")
        print("Пример (безопасный): python fixed_app.py \"2 + 2 * 3\"")
        print("Пример (НЕ СРАБОТАЕТ): python fixed_app.py \"__import__('os').system('echo HACKED!')\"")
        sys.exit(1)

    user_input = sys.argv[1]
    print(f"Получено выражение: {user_input}")
    safe_calculate(user_input) 