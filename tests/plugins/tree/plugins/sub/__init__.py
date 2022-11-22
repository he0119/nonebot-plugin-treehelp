from pathlib import Path

import nonebot
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="复杂功能",
    description="测试插件复杂子插件",
    usage="/复杂功能",
)

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "subsub").resolve()))
