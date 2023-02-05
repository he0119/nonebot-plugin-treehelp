from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="Fake",
    description="测试 Fake 适配器",
    usage="/fake",
    extra={
        "adapters": ["fake"],
    },
)
