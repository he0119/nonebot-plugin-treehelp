""" 帮助数据

获取插件的帮助信息，并通过子插件的形式获取次级菜单
"""
from typing import TYPE_CHECKING, Dict, List, Optional, Set

from nonebot import get_loaded_plugins

if TYPE_CHECKING:
    from nonebot.adapters import Bot
    from nonebot.plugin import Plugin

_plugins: Optional[Dict[str, "Plugin"]] = None


# def sort_commands(cmds: list[tuple[str, ...]]) -> list[tuple[str, ...]]:
#     """排序命令

#     确保英文名字在前，中文名字在后
#     命令越长越靠前
#     """
#     return sorted(
#         cmds,
#         key=lambda x: (
#             len("".join(x).encode("ascii", "ignore")),  # 英文在前
#             len(x),  # 命令越长越靠前
#             len("".join(x)),  # 命令字数越长越靠前
#         ),
#         reverse=True,
#     )


# def extract_command_info(matcher: "Matcher") -> Optional[CommandInfo]:
#     """从 Matcher 中提取命令的数据"""
#     checkers = matcher.rule.checkers
#     command_handler = next(
#         filter(lambda x: isinstance(x.call, CommandRule), checkers), None
#     )
#     if not command_handler:
#         return

#     help = matcher.__doc__
#     if help is None:
#         return
#     help = inspect.cleandoc(help)

#     command = cast(CommandRule, command_handler.call)
#     cmds = sort_commands(command.cmds)

#     name = ".".join(cmds[0])
#     if len(cmds) > 1:
#         aliases = list(map(lambda x: ".".join(x), cmds[1:]))
#     else:
#         aliases = []
#     return CommandInfo(name=name, aliases=aliases, help=help)


def format_description(plugins: List["Plugin"]) -> str:
    """格式化描述"""
    return "\n".join(
        sorted(
            map(
                lambda x: f"{x.metadata.name} # {x.metadata.description}",  # type: ignore
                plugins,
            )
        )
    )


def is_supported_adapter(bot: "Bot", plugin: "Plugin") -> bool:
    """是否是支持的适配器"""
    supported_adapters = plugin.metadata.extra.get("adapters")  # type: ignore
    if (
        supported_adapters  # 拥有 adapters 信息
        and isinstance(supported_adapters, (set, list))  # 并且是集合或列表
        and bot.adapter.get_name() not in supported_adapters  # 且当前适配器名不在集合中
    ):
        return False
    return True


def get_plugins() -> Dict[str, "Plugin"]:
    """获取适配了元信息的插件"""
    global _plugins

    if _plugins is None:
        plugins = filter(lambda x: x.metadata is not None, get_loaded_plugins())
        _plugins = {x.metadata.name: x for x in plugins}  # type: ignore

    return _plugins


def get_plugin_list(bot: "Bot", tree: bool = False) -> str:
    """获取插件列表"""
    # 仅保留根插件
    plugins = [
        plugin
        for plugin in get_plugins().values()
        if plugin.parent_plugin is None and is_supported_adapter(bot, plugin)
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
        return

    # 排除不支持的插件
    if not is_supported_adapter(bot, plugin):
        return

    if tree:
        docs = [f"{plugin.metadata.name} # {plugin.metadata.description}"]  # type: ignore
        get_tree_string(bot, docs, plugin.sub_plugins, "")
        return "\n".join(docs)

    usage = plugin.metadata.usage  # type: ignore
    sub_plugins = [
        plugin
        for plugin in plugin.sub_plugins
        if plugin.metadata is not None and is_supported_adapter(bot, plugin)
    ]
    sub_plugins_desc = format_description(sub_plugins)
    return "\n\n".join([x for x in [name, usage, sub_plugins_desc] if x])


def get_tree_string(
    bot: "Bot",
    docs: List[str],
    plugins: Set["Plugin"],
    previous_tree_bar: str,
) -> None:
    """通过递归获取树形结构的字符串"""
    previous_tree_bar = previous_tree_bar.replace("├", "│")

    filtered_plugins = filter(
        lambda x: x.metadata is not None and is_supported_adapter(bot, x), plugins
    )
    sorted_plugins = sorted(filtered_plugins, key=lambda x: x.metadata.name)  # type: ignore

    tree_bar = previous_tree_bar + "├"
    total = len(sorted_plugins)
    for i, plugin in enumerate(sorted_plugins, 1):
        if i == total:
            tree_bar = previous_tree_bar + "└"
        docs.append(f"{tree_bar}── {plugin.metadata.name} # {plugin.metadata.description}")  # type: ignore
        tree_bar = tree_bar.replace("└", " ")
        get_tree_string(bot, docs, plugin.sub_plugins, tree_bar + "   ")
