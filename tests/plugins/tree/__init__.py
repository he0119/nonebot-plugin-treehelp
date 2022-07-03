from pathlib import Path

import nonebot
from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

__plugin_meta__ = PluginMetadata(
    name="测试",
    description="一个测试插件",
    usage="",
    config=Config,
)

_sub_plugins = set()
_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "plugins").resolve()))
