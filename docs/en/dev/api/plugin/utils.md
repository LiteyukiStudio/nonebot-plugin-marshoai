---
title: utils
---
# **Module** `nonebot_plugin_marshoai.plugin.utils`

---
### ***func*** `path_to_module_name(path: Path) -> str`

**Description**: 转换路径为模块名

**Arguments**:
> - path: 路径a/b/c/d -> a.b.c.d  

**Return**: str: 模块名


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/utils.py#L6' target='_blank'>View on GitHub</a></summary>

```python
def path_to_module_name(path: Path) -> str:
    rel_path = path.resolve().relative_to(Path.cwd().resolve())
    if rel_path.stem == '__init__':
        return '.'.join(rel_path.parts[:-1])
    else:
        return '.'.join(rel_path.parts[:-1] + (rel_path.stem,))
```
</details>

---
### ***func*** `is_coroutine_callable(call: Callable[..., Any]) -> bool`

**Description**: 判断是否为async def 函数

**Arguments**:
> - call: 可调用对象  

**Return**: bool: 是否为协程可调用对象


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/utils.py#L21' target='_blank'>View on GitHub</a></summary>

```python
def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    func_ = getattr(call, '__call__', None)
    return inspect.iscoroutinefunction(func_)
```
</details>

