from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import Alconna, on_alconna

__plugin_meta__ = PluginMetadata(
    name="Alconna",
    description="测试插件 alconna 子插件",
    usage="/alconna",
)

alconna = on_alconna(Alconna("alconna"))
alconna.shortcut(
    "alc",
    {
        "prefix": True,
        "command": "alconna",
    },
)
