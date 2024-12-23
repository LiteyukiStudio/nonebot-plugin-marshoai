---
order: 1
---

# 项目开发

## 先决条件

- `Git`
- `Python3.10+`

## 准备工作

- 克隆仓库

```bash
git clone https://github.com/LiteyukiStudio/nonebot-plugin-marshoai.git # 克隆仓库
cd nonebot-plugin-marshoai  # 切换目录
```

- 安装依赖
项目使用pdm作为依赖管理

```bash
python3 -m venv venv    # 或创建你自己的环境
source venv/bin/activate    # 激活虚拟环境
pip install pdm # 安装依赖管理
pdm install # 安装依赖
pre-commit install  # 安装 pre-commit 钩子
```

## 代码规范

主仓库需要遵循以下代码规范

- [`PEP8`](https://peps.python.org/pep-0008/)    代码风格
- [`Black`](https://black.readthedocs.io/en/stable/index.html)   代码格式化
- [`mypy`](https://www.mypy-lang.org/) 静态类型检查
- [`Google Docstring`](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) 文档规范

可以在编辑器中安装相应的插件进行辅助

## 其他

感谢以下的贡献者们：

<ContributorsBar />

<script setup> import ContributorsBar from '../../components/ContributorsBar.vue' </script>