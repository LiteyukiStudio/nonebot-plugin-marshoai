---
title: mk_common
---
# **模块** `nonebot_plugin_marshoai.tools.marshoai_megakits.mk_common`

---
### ***async func*** `random_turntable(upper: int, lower: int)`

**说明**: Random Turntable


**参数**:
> - upper (int): _description_  
> - lower (int): _description_  

**返回**: _type_: _description_


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_common.py#L4' target='_blank'>在GitHub上查看</a></summary>

```python
async def random_turntable(upper: int, lower: int):
    return random.randint(lower, upper)
```
</details>

---
### ***async func*** `number_calc(a: str, b: str, op: str) -> str`

**说明**: Number Calc


**参数**:
> - a (str): _description_  
> - b (str): _description_  
> - op (str): _description_  

**返回**: str: _description_


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/tools/marshoai_megakits/mk_common.py#L17' target='_blank'>在GitHub上查看</a></summary>

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

