from nonebot import on_command, on_message
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="简单功能",
    description="测试插件简单子插件",
    usage="/简单功能",
)

simple = on_command("simple", aliases={("simple", "alias")}, priority=1, block=True)

simple_message = on_message()
