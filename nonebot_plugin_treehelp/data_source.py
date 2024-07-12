"""帮助数据

获取插件的帮助信息，并通过子插件的形式获取次级菜单
"""

from typing import TYPE_CHECKING, Optional, Union, cast

from nonebot import get_driver, get_loaded_plugins, require
from nonebot.rule import CommandRule, ShellCommandRule

try:
    require("nonebot_plugin_alconna")
    from nonebot_plugin_alconna import command_manager
    from nonebot_plugin_alconna.rule import AlconnaRule

    COMMAND_RULES = (CommandRule, ShellCommandRule, AlconnaRule)
except (ImportError, RuntimeError):  # pragma: no cover
    command_manager = None
    AlconnaRule = None
    COMMAND_RULES = (CommandRule, ShellCommandRule)

from .config import plugin_config

if TYPE_CHECKING:
    from nonebot.adapters import Bot
    from nonebot.plugin import Plugin, PluginMetadata

global_config = get_driver().config

_plugins: Optional[dict[str, "Plugin"]] = None
_commands: dict[tuple[str, ...], "Plugin"] = {}


def map_command_to_plguin(plugin: "Plugin"):
    """建立命令与插件的映射"""
    matchers = plugin.matcher
    for matcher in matchers:
        checkers = matcher.rule.checkers
        command_handler = next(
            filter(lambda x: isinstance(x.call, COMMAND_RULES), checkers),
            None,
        )
        if not command_handler:
            continue

        if (
            AlconnaRule
            and isinstance(command_handler.call, AlconnaRule)
            and command_manager
        ):
            command = command_handler.call.command()
            if not command:  # pragma: no cover
                continue

            cmds = [(str(command.command),)]
            shortcuts = command_manager.get_shortcut(command)
            cmds.extend([(shortcut,) for shortcut in shortcuts])

        else:
            command = cast(Union[CommandRule, ShellCommandRule], command_handler.call)
            cmds = command.cmds

        for cmd in cmds:
            _commands[cmd] = plugin


def format_description(plugins: list["Plugin"]) -> str:
    """格式化描述"""
    return "\n".join(
        sorted(f"{x.metadata.name} # {x.metadata.description}" for x in plugins)  # type: ignore
    )


def is_supported_adapter(bot: "Bot", metadata: "PluginMetadata") -> bool:
    """是否是支持的适配器"""
    if metadata.supported_adapters is None:
        return True

    supported_adapters = metadata.get_supported_adapters()
    if not supported_adapters:
        return False

    for adapter in supported_adapters:
        if isinstance(bot.adapter, adapter):
            return True

    return False


def is_supported_type(metadata: "PluginMetadata") -> bool:
    """是否是支持的插件类型

    当前有 library 和 application 两种类型
    仅支持 application 类型的插件
    """
    type_ = metadata.type
    # 如果没有指定类型，则默认支持
    if type_ is None:
        return True
    # 当前仅支持 application 类型
    if type_ == "application":
        return True
    return False


def is_supported(bot: "Bot", plugin: "Plugin") -> bool:
    """是否是支持的插件"""
    if plugin.metadata is None:
        return False

    if plugin.metadata.name in plugin_config.treehelp_ignored_plugins:
        return False

    if not is_supported_type(plugin.metadata):
        return False

    if not is_supported_adapter(bot, plugin.metadata):
        return False

    return True


def get_plugins() -> dict[str, "Plugin"]:
    """获取适配了元信息的插件"""
    global _plugins

    if _plugins is None:
        plugins = filter(lambda x: x.metadata is not None, get_loaded_plugins())
        _plugins = {x.metadata.name: x for x in plugins}  # type: ignore
        for plugin in _plugins.values():
            map_command_to_plguin(plugin)

    return _plugins


def get_plugin_list(bot: "Bot", tree: bool = False) -> str:
    """获取插件列表"""
    # 仅保留根插件
    plugins = [
        plugin
        for plugin in get_plugins().values()
        if plugin.parent_plugin is None and is_supported(bot, plugin)
    ]
    sorted_plugins = sorted(plugins, key=lambda x: x.metadata.name)  # type: ignore

    docs = ["插件："]
    if tree:
        for plugin in sorted_plugins:
            docs.append(f"{plugin.metadata.name} # {plugin.metadata.description}")  # type: ignore
            get_tree_string(bot, docs, plugin.sub_plugins, "")
    else:
        docs.append(format_description(sorted_plugins))
    return "\n".join(docs)


def get_plugin_help(bot: "Bot", name: str, tree: bool = False) -> Optional[str]:
    """通过插件获取命令的帮助"""
    plugins = get_plugins()

    plugin = plugins.get(name)
    if not plugin:
        # str.split 只支持单个分隔符
        # 用 re 又太麻烦了，直接遍历所有分隔符，找到就停止
        for sep in global_config.command_sep:
            plugin = _commands.get(tuple(name.split(sep)))
            if plugin:
                break
    if not plugin:
        return

    # 排除不支持的插件
    if not is_supported(bot, plugin):
        return

    metadata = cast("PluginMetadata", plugin.metadata)

    if tree:
        docs = [f"{metadata.name} # {metadata.description}"]
        get_tree_string(bot, docs, plugin.sub_plugins, "")
        return "\n".join(docs)

    sub_plugins = [plugin for plugin in plugin.sub_plugins if is_supported(bot, plugin)]
    sub_plugins_desc = format_description(sub_plugins)
    return "\n\n".join(
        [x for x in [metadata.name, metadata.usage, sub_plugins_desc] if x]
    )


def get_tree_string(
    bot: "Bot",
    docs: list[str],
    plugins: set["Plugin"],
    previous_tree_bar: str,
) -> None:
    """通过递归获取树形结构的字符串"""
    previous_tree_bar = previous_tree_bar.replace("├", "│")

    filtered_plugins = filter(lambda x: is_supported(bot, x), plugins)
    sorted_plugins = sorted(filtered_plugins, key=lambda x: x.metadata.name)  # type: ignore

    tree_bar = previous_tree_bar + "├"
    total = len(sorted_plugins)
    for i, plugin in enumerate(sorted_plugins, 1):
        if i == total:
            tree_bar = previous_tree_bar + "└"
        docs.append(
            f"{tree_bar}── {plugin.metadata.name} # {plugin.metadata.description}"  # type: ignore
        )
        tree_bar = tree_bar.replace("└", " ")
        get_tree_string(bot, docs, plugin.sub_plugins, tree_bar + "   ")
