---
title: load
---
# **Module** `nonebot_plugin_marshoai.plugin.load`

Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved
本模块为工具加载模块


---
### ***func*** `get_plugin(name: str) -> Plugin | None`

**Description**: 获取插件对象


**Arguments**:
> - name: 插件名称  

**Return**: Optional[Plugin]: 插件对象


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L26' target='_blank'>View on GitHub</a></summary>

```python
def get_plugin(name: str) -> Plugin | None:
    return _plugins.get(name)
```
</details>

---
### ***func*** `get_plugins() -> dict[str, Plugin]`

**Description**: 获取所有插件


**Return**: dict[str, Plugin]: 插件集合


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L37' target='_blank'>View on GitHub</a></summary>

```python
def get_plugins() -> dict[str, Plugin]:
    return _plugins
```
</details>

---
### ***func*** `load_plugin(module_path: str | Path) -> Optional[Plugin]`

**Description**: 加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。
该函数产生的副作用在于将插件加载到 `_plugins` 中。


**Arguments**:
> - module_path: 插件名称 `path.to.your.plugin`  
> - 或插件路径 `pathlib.Path(path/to/your/plugin)`:   

**Return**: Optional[Plugin]: 插件对象


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L46' target='_blank'>View on GitHub</a></summary>

```python
def load_plugin(module_path: str | Path) -> Optional[Plugin]:
    module_path = path_to_module_name(Path(module_path)) if isinstance(module_path, Path) else module_path
    try:
        module = import_module(module_path)
        plugin = Plugin(name=module.__name__, module=module, module_name=module_path)
        _plugins[plugin.name] = plugin
        plugin.metadata = getattr(module, '__marsho_meta__', None)
        if plugin.metadata is None:
            logger.opt(colors=True).warning(f'成功加载小棉插件 <y>{plugin.name}</y>, 但是没有定义元数据')
        else:
            logger.opt(colors=True).success(f'成功加载小棉插件 <c>"{plugin.metadata.name}"</c>')
        return plugin
    except Exception as e:
        logger.opt(colors=True).success(f'加载小棉插件失败 "<r>{module_path}</r>"')
        traceback.print_exc()
        return None
```
</details>

---
### ***func*** `load_plugins(*plugin_dirs: str) -> set[Plugin]`

**Description**: 导入文件夹下多个插件


**Arguments**:
> - plugin_dir: 文件夹路径  
> - ignore_warning: 是否忽略警告，通常是目录不存在或目录为空  

**Return**: set[Plugin]: 插件集合


<details>
<summary> <b>Source code</b> or <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L89' target='_blank'>View on GitHub</a></summary>

```python
def load_plugins(*plugin_dirs: str) -> set[Plugin]:
    plugins = set()
    for plugin_dir in plugin_dirs:
        for f in os.listdir(plugin_dir):
            path = Path(os.path.join(plugin_dir, f))
            module_name = None
            if os.path.isfile(path) and f.endswith('.py'):
                '单文件加载'
                module_name = f'{path_to_module_name(Path(plugin_dir))}.{f[:-3]}'
            elif os.path.isdir(path) and os.path.exists(os.path.join(path, '__init__.py')):
                '包加载'
                module_name = path_to_module_name(path)
            if module_name and (plugin := load_plugin(module_name)):
                plugins.add(plugin)
    return plugins
```
</details>

### var `module`

- **Description**: 导入模块对象

- **Default**: `import_module(module_path)`

### var `module_name`

- **Description**: 单文件加载

- **Default**: `f'{path_to_module_name(Path(plugin_dir))}.{f[:-3]}'`

### var `module_name`

- **Description**: 包加载

- **Default**: `path_to_module_name(path)`

