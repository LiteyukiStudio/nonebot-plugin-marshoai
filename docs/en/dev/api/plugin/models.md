---
title: models
---
# **Module** `nonebot_plugin_marshoai.plugin.models`

### ***class*** `PluginMetadata(BaseModel)`
#### ***attr*** `name: str = NO_DEFAULT`

#### ***attr*** `description: str = ''`

#### ***attr*** `usage: str = ''`

#### ***attr*** `author: str = ''`

#### ***attr*** `homepage: str = ''`

#### ***attr*** `extra: dict[str, Any] = {}`

### ***class*** `Plugin(BaseModel)`
---
#### ***func*** `hash self => int`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/models.py#L67' target='_blank'>View on GitHub</a></summary>

```python
def __hash__(self) -> int:
    return hash(self.name)
```
</details>

---
#### ***func*** `self == other: Any => bool`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/models.py#L70' target='_blank'>View on GitHub</a></summary>

```python
def __eq__(self, other: Any) -> bool:
    return self.name == other.name
```
</details>

#### ***attr*** `name: str = NO_DEFAULT`

#### ***attr*** `module: ModuleType = NO_DEFAULT`

#### ***attr*** `module_name: str = NO_DEFAULT`

#### ***attr*** `metadata: PluginMetadata | None = None`

### ***class*** `FunctionCallArgument(BaseModel)`
---
#### ***func*** `data(self) -> dict[str, Any]`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/models.py#L95' target='_blank'>View on GitHub</a></summary>

```python
def data(self) -> dict[str, Any]:
    return {'type': self.type_, 'description': self.description}
```
</details>

#### ***attr*** `type_: str = NO_DEFAULT`

#### ***attr*** `description: str = NO_DEFAULT`

#### ***attr*** `default: Any = None`

### ***class*** `FunctionCall(BaseModel)`
---
#### ***func*** `hash self => int`


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/models.py#L123' target='_blank'>View on GitHub</a></summary>

```python
def __hash__(self) -> int:
    return hash(self.name)
```
</details>

---
#### ***func*** `data(self) -> dict[str, Any]`

**Description**: 生成函数描述信息


**Return**: dict[str, Any]: 函数描述信息 字典


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/models.py#L126' target='_blank'>View on GitHub</a></summary>

```python
def data(self) -> dict[str, Any]:
    return {'type': 'function', 'function': {'name': self.name, 'description': self.description, 'parameters': {'type': 'object', 'properties': {k: v.data() for k, v in self.arguments.items()}}, 'required': [k for k, v in self.arguments.items() if v.default is None]}}
```
</details>

#### ***attr*** `name: str = NO_DEFAULT`

#### ***attr*** `description: str = NO_DEFAULT`

#### ***attr*** `arguments: dict[str, FunctionCallArgument] = NO_DEFAULT`

#### ***attr*** `function: ASYNC_FUNCTION_CALL_FUNC = NO_DEFAULT`

