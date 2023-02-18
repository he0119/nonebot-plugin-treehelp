<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin TreeHelp

_✨ NoneBot 树形帮助插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/he0119/nonebot-plugin-treehelp/main/LICENSE">
    <img src="https://img.shields.io/github/license/he0119/nonebot-plugin-treehelp.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-treehelp">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-treehelp.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
  <a href="https://codecov.io/gh/he0119/nonebot-plugin-treehelp">
    <img src="https://codecov.io/gh/he0119/nonebot-plugin-treehelp/branch/main/graph/badge.svg?token=jd5ufc1alv"/>
  </a>
  <a href="https://jq.qq.com/?_wv=1027&k=7zQUpiGp">
    <img src="https://img.shields.io/badge/QQ%E7%BE%A4-730374631-orange?style=flat-square" alt="QQ Chat Group">
  </a>
</p>

## 简介

使用插件元数据获取插件信息，并通过插件与子插件的组织形式，来区分插件的多种功能。

树形帮助插件，最重要的功能当然是显示插件树！

发送 `/help --tree`，你将获得如下帮助：

```text
插件：
帮助 # 获取插件帮助信息
测试 # 一个测试插件
├── 复杂功能 # 测试插件复杂子插件
│   └── 二级功能 # 测试插件二级插件
└── 简单功能 # 测试插件简单子插件
```

## 使用方式

加载插件后发送 `/help` 或 `/help --help` 获取具体用法。

插件与子插件写法可参考 [示例插件](./tests/plugins/tree/)。

## 配置项

配置方式：直接在 `NoneBot` 全局配置文件中添加以下配置项即可。

暂时还没有可配置的东西。

## 计划

- [ ] 支持输出插件版本
- [x] 支持输出插件树
- [ ] 支持输出插件内的命令名称
