from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="library",
    description="测试库插件",
    usage="/library",
    supported_adapters={"~console"},
    type="library",
)
