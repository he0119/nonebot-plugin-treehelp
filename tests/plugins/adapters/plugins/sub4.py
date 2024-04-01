"""插件支持的适配器不存在"""

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="Console",
    description="测试 Console 适配器",
    usage="/console",
    supported_adapters={"~fake"},
)
