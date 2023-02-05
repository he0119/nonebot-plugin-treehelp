""" 帮助

通过读取插件元信息生成帮助信息
"""
from nonebot import on_command
from nonebot.adapters import Bot, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .data_source import get_plugin_help, get_plugin_list, get_tree_view

__plugin_meta__ = PluginMetadata(
    name="帮助",
    description="获取插件帮助信息",
    usage="""获取插件列表
/help list
获取某个插件的帮助
/help 插件名
获取插件树
/help tree""",
)

help_cmd = on_command("help", aliases={"帮助"})


@help_cmd.handle()
async def help_handle(bot: Bot, args: Message = CommandArg()):
    plaintext = args.extract_plain_text().strip()

    if plaintext in ["list", "列表"]:
        await help_cmd.finish(get_plugin_list(bot))
    elif plaintext in ["tree", "树"]:
        await help_cmd.finish(get_tree_view(bot))
    elif plaintext:
        command_help = get_plugin_help(plaintext, bot)
        if command_help:
            await help_cmd.finish(command_help)
        await help_cmd.finish("请输入支持的插件名")
    else:
        await help_cmd.finish(get_plugin_help("帮助", bot))
