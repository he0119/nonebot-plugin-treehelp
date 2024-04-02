"""帮助

通过读取插件元信息生成帮助信息
"""

from nonebot import on_shell_command
from nonebot.adapters import Bot
from nonebot.exception import ParserExit
from nonebot.params import ShellCommandArgs
from nonebot.plugin import PluginMetadata
from nonebot.rule import ArgumentParser, Namespace

from .config import Config
from .data_source import get_plugin_help, get_plugin_list

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="获取插件帮助信息",
    usage="""获取插件列表
/help
获取插件树
/help -t
/help --tree
获取某个插件的帮助
/help 插件名
获取某个插件的树
/help --tree 插件名
""",
    type="application",
    homepage="https://github.com/he0119/nonebot-plugin-treehelp",
    config=Config,
)

parser = ArgumentParser("帮助", description="获取插件帮助信息")
parser.add_argument("plugin_name", nargs="?", type=str, help="插件名", metavar="插件名")
parser.add_argument("-t", "--tree", action="store_true", help="获取插件树")
help_cmd = on_shell_command("help", aliases={"帮助"}, parser=parser)


@help_cmd.handle()
async def help_handle(bot: Bot, args: Namespace = ShellCommandArgs()):
    plugin_name = args.plugin_name

    if plugin_name is None:
        await help_cmd.finish(get_plugin_list(bot, args.tree))

    plugin_help = get_plugin_help(bot, plugin_name, args.tree)
    if plugin_help:
        await help_cmd.finish(plugin_help)
    else:
        await help_cmd.finish(f"未找到插件 {plugin_name}")


@help_cmd.handle()
async def _(foo: ParserExit = ShellCommandArgs()):
    await help_cmd.finish(foo.message)
