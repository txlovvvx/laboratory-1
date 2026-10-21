import re

def interpret(text):
    tokens = re.findall(r'\d+\.\d+|\d+|\w+|[-+*/^(),]', text)
    pos = 0

    def current():
        return tokens[pos] if pos < len(tokens) else None

    def advance():
        nonlocal pos
        pos += 1

    def parse_factor():
        nonlocal pos
        token = current()
        
        
        if token == '-':
            advance()
            return -parse_factor()
        if token == '+':
            advance()
            return parse_factor()
            

        if token == '(':
            advance()
            val = parse_xor()
            advance() # пропускаем ')'
            return val
            
        if token and token.isalpha():
            func_name = token
            advance() # имя функции
            advance() # открывающая скобка '('
            
            args = []
            if current() != ')':
                args.append(parse_xor())
                while current() == ',':
                    advance() # запятая
                    args.append(parse_xor())
            advance() # закрывающая скобка ')'
            
            if func_name == 'max':
                if not args:
                    raise ValueError("функция max() требует хотя бы один аргумент")
                return max(args)
            raise ValueError(f"неизвестная функция: {func_name}")
            
        
        if token is None:
            raise ValueError("недопустимые функции или символы в выражении")
        advance()
        return float(token) if '.' in token else int(token)

    def parse_term():
        val = parse_factor()
        while current() in ('*', '/'):
            op = current()
            advance()
            if op == '*':
                val *= parse_factor()
            else:
                divisor = parse_factor()
                if divisor == 0:
                    raise ZeroDivisionError("деление на ноль")
                val /= divisor
        return val

    def parse_expr():
        val = parse_term()
        while current() in ('+', '-'):
            op = current()
            advance()
            if op == '+':
                val += parse_term()
            else:
                val -= parse_term()
        return val

    def parse_xor():
        val = parse_expr()
        while current() == '^':
            advance()
            val = int(val) ^ int(parse_expr())
        return val

    if not tokens:
        return 0
    return parse_xor()

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("       интерпритатор арифметических выражений     ")
    print("--------------------------------------------------")
    print("         доступные знаки и функции:")
    print("  сложение (+) и вычитание (-)")
    print("  умножение (*) и деление (/)")
    print("  унарный минус и плюс (например, -5 или +3)")
    print("  круглые скобки (...) для изменения приоритета")
    print("  функция max(x, y, ...) — поиск максимума")
    print("  побитовый XOR (^) — исключающее ИЛИ")
    print("--------------------------------------------------")
    print("пример ввода: max(10, 25.5, 7) ^ 2")
    print("--------------------------------------------------\n")
    
    while True:
        user_input = input("введите математическое выражение: ").strip()
        
            
        if not user_input:
            continue
        try:
            result = interpret(user_input)
            print(f"результат вычислений: {result}\n")
        except Exception as e:
            print(f"ошибка при вычислении: {e}\n")