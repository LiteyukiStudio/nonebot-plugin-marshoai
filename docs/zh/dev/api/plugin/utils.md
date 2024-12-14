---
title: utils
---
# **模块** `nonebot_plugin_marshoai.plugin.utils`

---
### ***func*** `path_to_module_name(path: Path) -> str`

**说明**: 转换路径为模块名

**参数**:
> - path: 路径a/b/c/d -> a.b.c.d  

**返回**: str: 模块名


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/utils.py#L6' target='_blank'>在GitHub上查看</a></summary>

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

**说明**: 判断是否为async def 函数

**参数**:
> - call: 可调用对象  

**返回**: bool: 是否为协程可调用对象


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/utils.py#L21' target='_blank'>在GitHub上查看</a></summary>

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

