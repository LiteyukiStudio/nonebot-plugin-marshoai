# 开发指北

## 规范

- PEP8
- mypy 类型检查
- black 格式化

## 开发依赖

- pre-commit，确保代码质量合格才可以提交

```bash
pre-commit install
```

## 其他提示

- 请勿在大小写不敏感的文件系统或操作系统中开发，否则可能会导致文件名大小写问题(例如Windows， APFS(不区分大小写)等)