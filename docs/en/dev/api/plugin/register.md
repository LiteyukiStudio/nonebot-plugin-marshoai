---
title: register
---
# **Module** `nonebot_plugin_marshoai.plugin.register`

此模块用于获取function call中函数定义信息以及注册函数


---
### ***func*** `async_wrapper(func: SYNC_FUNCTION_CALL_FUNC) -> ASYNC_FUNCTION_CALL_FUNC`

**Description**: 将同步函数包装为异步函数，但是不会真正异步执行，仅用于统一调用及函数签名


**Arguments**:
> - func: 同步函数  

**Return**: ASYNC_FUNCTION_CALL: 异步函数


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/register.py#L20' target='_blank'>View on GitHub</a></summary>

```python
def async_wrapper(func: SYNC_FUNCTION_CALL_FUNC) -> ASYNC_FUNCTION_CALL_FUNC:

    async def wrapper(*args, **kwargs) -> str:
        return func(*args, **kwargs)
    return wrapper
```
</details>

---
### ***func*** `function_call(*funcs: FUNCTION_CALL_FUNC) -> None`


**Arguments**:
> - func: 函数对象，要有完整的 Google Style Docstring  

**Return**: str: 函数定义信息


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/register.py#L36' target='_blank'>View on GitHub</a></summary>

```python
def function_call(*funcs: FUNCTION_CALL_FUNC) -> None:
    for func in funcs:
        function_call = get_function_info(func)
```
</details>

---
### ***func*** `get_function_info(func: FUNCTION_CALL_FUNC)`

**Description**: 获取函数信息


**Arguments**:
> - func: 函数对象  

**Return**: FunctionCall: 函数信息对象模型


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/register.py#L50' target='_blank'>View on GitHub</a></summary>

```python
def get_function_info(func: FUNCTION_CALL_FUNC):
    name = func.__name__
    description = func.__doc__
    logger.info(f'注册函数: {name} {description}')
```
</details>

