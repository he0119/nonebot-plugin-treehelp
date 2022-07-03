""" 帮助数据

获取插件的帮助信息，并通过子插件的形式获取次级菜单
"""
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional

from nonebot import get_loaded_plugins

if TYPE_CHECKING:
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


def get_plugins() -> Dict[str, "Plugin"]:
    """获取适配了元信息的插件"""
    global _plugins

    if _plugins is None:
        plugins = filter(lambda x: x.metadata is not None, get_loaded_plugins())
        _plugins = {x.metadata.name: x for x in plugins}  # type: ignore

    return _plugins


def get_plugin_list() -> str:
    """获取插件列表"""
    # 仅保留根插件
    plugins = [
        plugin for plugin in get_plugins().values() if plugin.parent_plugin is None
    ]

    docs = "插件列表：\n"
    docs += format_description(plugins)
    return docs


def get_plugin_help(name: str) -> Optional[str]:
    """通过插件获取命令的帮助"""
    plugins = get_plugins()

    plugin = plugins.get(name)
    if not plugin:
        return

    usage = plugin.metadata.usage  # type: ignore

    sub_plugins = [
        plugin for plugin in plugin.sub_plugins if plugin.metadata is not None
    ]
    sub_plugins_desc = format_description(sub_plugins)

    return "\n\n".join([x for x in [name, usage, sub_plugins_desc] if x])
