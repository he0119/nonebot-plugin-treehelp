from pathlib import Path

import nonebot
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="测试",
    description="一个测试插件",
    usage="",
)

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "plugins").resolve()))
