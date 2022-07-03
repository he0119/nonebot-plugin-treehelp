import pytest
from nonebug import App

from .utils import make_fake_event, make_fake_message


@pytest.mark.asyncio
async def test_root(app: App):
    """测试帮助"""
    from nonebot import require

    require("tests.plugins.tree")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help list")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件列表：\n帮助 # 获取插件帮助信息\n测试 # 一个测试插件", True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_sub_plugins(app: App):
    """测试帮助"""
    from nonebot import require

    require("tests.plugins.tree")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help 测试")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "测试\n\n功能一 # 测试插件子插件一", True)
        ctx.should_finished()
