from nonebug import App
from pytest_mock import MockerFixture

from .utils import make_fake_event, make_fake_message


async def test_ignored(app: App, mocker: MockerFixture):
    """通过插件名称忽略指定插件"""
    from nonebot import require

    from nonebot_plugin_treehelp.config import plugin_config

    mocker.patch.object(plugin_config, "treehelp_ignored_plugins", ["帮助"])

    require("tests.plugins.adapters")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件：\n适配器 # 测试不同适配器", True)
        ctx.should_finished()
