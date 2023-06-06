from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="OneBot",
    description="测试 OneBot 适配器",
    usage="/onebot",
    supported_adapters={"~onebot.v11", "~onebot.v12"},
)
