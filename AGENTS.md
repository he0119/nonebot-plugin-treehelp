# NoneBot 树形帮助插件 AI 编码指南

欢迎来到 `nonebot-plugin-treehelp` 项目！本指南旨在帮助 AI 编码代理快速理解项目结构、关键组件和开发工作流程。

## 1. 项目概述

本项目是一个为 [NoneBot2](https://v2.nonebot.dev/) 框架开发的树形帮助插件。它通过读取已加载插件的 `PluginMetadata`，生成插件列表、插件帮助和插件树。

- **核心功能**: 根据插件元信息输出插件名称、描述、用法，并通过 `parent_plugin` / `sub_plugins` 组织树形结构。
- **命令系统**: 使用 `on_shell_command("help", aliases={"帮助"})` 注册 `/help` / `帮助` 命令，并通过 `ArgumentParser` 解析插件名和 `--tree` 参数。
- **命令反查**: 支持通过命令名查找对应插件，兼容 NoneBot 内置 `CommandRule`、`ShellCommandRule`，并在安装 `nonebot-plugin-alconna` 时额外支持 `AlconnaRule` 与快捷命令。
- **插件过滤**: 根据插件类型、适配器支持范围和 `treehelp_ignored_plugins` 配置过滤展示结果。
- **适配器兼容**: 通过 `PluginMetadata.supported_adapters` 判断当前 `Bot` 所属适配器是否应展示某插件。

## 2. 关键模块与代码结构

理解以下文件是快速上手的关键：

- **`nonebot_plugin_treehelp/__init__.py`**: 插件主入口。定义 `PluginMetadata`、帮助命令参数解析器和命令处理器。修改用户可见命令、帮助文本、参数行为时优先从这里开始。
- **`nonebot_plugin_treehelp/data_source.py`**: 帮助内容生成的核心逻辑。负责加载插件、建立命令到插件的映射、过滤插件、格式化普通列表和递归生成树形输出。
- **`nonebot_plugin_treehelp/config.py`**: 定义插件配置项。当前只有 `treehelp_ignored_plugins`，用于从帮助列表和插件树中隐藏指定插件。
- **`tests/`**: 测试目录。使用 `nonebug` 构造 NoneBot 测试应用，覆盖基础帮助、插件树、嵌套子插件、忽略插件、适配器过滤和 Alconna 命令映射。
- **`tests/plugins/`**: 测试用插件集合。新增或调整插件树行为时，优先在这里添加最小测试插件，而不是依赖真实外部插件。

## 3. 开发工作流

- **依赖管理**: 项目使用 `uv` 管理依赖，构建后端为 `uv_build`。运行时依赖和开发依赖都在 `pyproject.toml` 中定义，开发依赖位于 `[dependency-groups]`。
- **Python 版本**: 当前最低支持 Python 3.10，类型标注可使用 `str | None`、`list[str]` 等现代写法。
- **测试**: 测试使用 `pytest`、`nonebug` 和 `pytest-xdist`。运行测试的命令定义在 `pyproject.toml` 的 `[tool.poe.tasks]` 部分。
  - 运行所有测试: `uv run poe test`
- **类型与格式**: `pyright` 目标版本为 Python 3.10，`ruff` target 为 `py310`。保持现有导入排序、行宽和 lint 规则。
- **提交与 PR**:
  - 提交信息和 PR 标题使用约定式提交格式，例如 `fix: 修复 Alconna 快捷命令帮助映射`。
  - PR 标题和正文使用中文，正文需说明变更内容、影响和验证命令。
  - 涉及用户可见功能、修复或行为变化时，在提交前同步维护 `CHANGELOG.md` 的 `Unreleased` 小节。

## 4. 重要模式与约定

- **插件元信息是唯一展示来源**:

  - 只有存在 `PluginMetadata` 的插件才会进入帮助系统。
  - 普通列表和树形列表都应展示 `metadata.name` 与 `metadata.description`。
  - 单插件帮助输出由插件名、`metadata.usage` 和可见子插件描述组成。

- **插件过滤规则**:

  - `metadata.type` 为空时默认展示。
  - `metadata.type == "application"` 时展示。
  - `metadata.type == "library"` 或其它类型时不展示。
  - `metadata.name` 出现在 `treehelp_ignored_plugins` 时不展示。
  - 设置了 `supported_adapters` 的插件，只在当前 `Bot` 适配器匹配时展示。

- **插件树生成**:

  - 根列表只展示 `parent_plugin is None` 的插件。
  - 子插件通过 `plugin.sub_plugins` 递归输出。
  - 树形字符当前使用 `├──`、`└──` 和 `│` 组合；修改格式时同步更新树相关测试。
  - 排序使用插件展示名称，保持输出稳定。

- **命令到插件的映射**:

  - `get_plugins()` 首次执行时会缓存插件并填充 `_commands`。
  - 内置命令规则从 `CommandRule` / `ShellCommandRule` 的 `cmds` 读取。
  - Alconna 支持是可选能力，导入失败或运行时不可用时必须优雅降级。
  - 通过命令名查找插件时会使用 `global_config.command_sep` 拆分命令；测试中配置了 `"."` 和 `"。"`。

- **测试隔离**:

  - `tests/utils.py` 的 `clear_plugins()` 会清理 NoneBot 插件注册和相关模块缓存。
  - `tests/conftest.py` 每个测试重新加载 `nonebot_plugin_treehelp`，并注册 Console、OneBot V11、OneBot V12 适配器。
  - 新增测试时优先复用 `make_fake_message()`、`make_fake_event()` 和 `nonebug` 的 `app.test_matcher(...)` 模式。

- **配置**:

  - 不要硬编码可变过滤规则。需要用户配置的行为应添加到 `config.py` 的 `Config` 模型中，并提供合理默认值。
  - 修改配置项时同步更新 README 的配置说明和相关测试。

- **兼容性**:
  - `nonebot-plugin-alconna` 是可选依赖，任何 Alconna 相关修改都要保持未安装时的基本帮助功能可用。
  - 插件不应引入数据库、网络请求或持久化副作用；帮助内容应只来自当前 NoneBot 运行时加载的插件信息。

在开始编码前，请确保你已熟悉 NoneBot2 的插件元信息、插件层级关系和命令规则机制。
