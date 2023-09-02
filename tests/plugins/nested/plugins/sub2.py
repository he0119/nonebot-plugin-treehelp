from nonebot.plugin import PluginMetadata

from .sub1 import plugin_id  # noqa: F401

__plugin_meta__ = PluginMetadata(
    name="功能二",
    description="测试插件子插件二",
    usage="/功能二",
)
