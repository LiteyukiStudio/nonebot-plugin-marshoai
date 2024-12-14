---
title: mk_common
---
# **Module** `nonebot_plugin_marshoai.tools.marshoai_megakits.mk_common`

---
### ***async func*** `random_turntable(upper: int, lower: int)`

**Description**: Random Turntable


**Arguments**:
> - upper (int): _description_  
> - lower (int): _description_  

**Return**: _type_: _description_


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_common.py#L4' target='_blank'>View on GitHub</a></summary>

```python
async def random_turntable(upper: int, lower: int):
    return random.randint(lower, upper)
```
</details>

---
### ***async func*** `number_calc(a: str, b: str, op: str) -> str`

**Description**: Number Calc


**Arguments**:
> - a (str): _description_  
> - b (str): _description_  
> - op (str): _description_  

**Return**: str: _description_


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_common.py#L17' target='_blank'>View on GitHub</a></summary>

```python
async def number_calc(a: str, b: str, op: str) -> str:
    a, b = (float(a), float(b))
    match op:
        case '+':
            return str(a + b)
        case '-':
            return str(a - b)
        case '*':
            return str(a * b)
        case '/':
            return str(a / b)
        case '**':
            return str(a ** b)
        case '%':
            return str(a % b)
        case _:
            return '未知运算符'
```
</details>

