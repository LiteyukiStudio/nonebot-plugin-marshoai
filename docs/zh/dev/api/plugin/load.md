---
title: load
---
# **模块** `nonebot_plugin_marshoai.plugin.load`

Copyright (C) 2020-2024 LiteyukiStudio. All Rights Reserved
本模块为工具加载模块


---
### ***func*** `get_plugin(name: str) -> Plugin | None`

**说明**: 获取插件对象


**参数**:
> - name: 插件名称  

**返回**: Optional[Plugin]: 插件对象


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L26' target='_blank'>在GitHub上查看</a></summary>

```python
def get_plugin(name: str) -> Plugin | None:
    return _plugins.get(name)
```
</details>

---
### ***func*** `get_plugins() -> dict[str, Plugin]`

**说明**: 获取所有插件


**返回**: dict[str, Plugin]: 插件集合


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L37' target='_blank'>在GitHub上查看</a></summary>

```python
def get_plugins() -> dict[str, Plugin]:
    return _plugins
```
</details>

---
### ***func*** `load_plugin(module_path: str | Path) -> Optional[Plugin]`

**说明**: 加载单个插件，可以是本地插件或是通过 `pip` 安装的插件。
该函数产生的副作用在于将插件加载到 `_plugins` 中。


**参数**:
> - module_path: 插件名称 `path.to.your.plugin`  
> - 或插件路径 `pathlib.Path(path/to/your/plugin)`:   

**返回**: Optional[Plugin]: 插件对象


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L46' target='_blank'>在GitHub上查看</a></summary>

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

**说明**: 导入文件夹下多个插件


**参数**:
> - plugin_dir: 文件夹路径  
> - ignore_warning: 是否忽略警告，通常是目录不存在或目录为空  

**返回**: set[Plugin]: 插件集合


<details>
<summary> <b>源代码</b> 或 <a href='https://github.com/LiteyukiStudio/nonebot-plugin-marshoai/tree/main/nonebot_plugin_marshoai/plugin/load.py#L89' target='_blank'>在GitHub上查看</a></summary>

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

- **说明**: 导入模块对象

- **默认值**: `import_module(module_path)`

### var `module_name`

- **说明**: 单文件加载

- **默认值**: `f'{path_to_module_name(Path(plugin_dir))}.{f[:-3]}'`

### var `module_name`

- **说明**: 包加载

- **默认值**: `path_to_module_name(path)`

