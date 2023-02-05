from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="OneBot",
    description="测试 OneBot 适配器",
    usage="/onebot",
    extra={
        "adapters": ["OneBot"],
    },
)
