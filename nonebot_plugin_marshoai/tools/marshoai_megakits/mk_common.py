import random


async def random_turntable(upper: int, lower: int):
    """Random Turntable

    Args:
        upper (int): _description_
        lower (int): _description_

    Returns:
        _type_: _description_
    """
    return random.randint(lower, upper)


async def number_calc(a: str, b: str, op: str) -> str:
    """Number Calc

    Args:
        a (str): _description_
        b (str): _description_
        op (str): _description_

    Returns:
        str: _description_
    """
    a, b = float(a), float(b)  # type: ignore
    match op:
        case "+":
            return str(a + b)  # type: ignore
        case "-":
            return str(a - b)  # type: ignore
        case "*":
            return str(a * b)  # type: ignore
        case "/":
            return str(a / b)  # type: ignore
        case "**":
            return str(a**b)  # type: ignore
        case "%":
            return str(a % b)
        case _:
            return "未知运算符"
