import random

# Random Turntable
async def random_turntable(upper: int, lower: int = "0"):
    return random.randint(lower, upper)

# Number Calc
def number_calc(a: str, b: str, op: str):
    a, b = float(a), float(b)
    match op:
        case "+":
            return str(a + b)
        case "-":
            return str(a - b)
        case "*":
            return str(a * b)
        case "/":
            return str(a / b)
        case "**":
            return str(a ** b)
        case "%":
            return str(a % b)
        case _:
            return "未知运算符"