import pytest
from nonebug import App

from .utils import make_fake_event, make_fake_message


@pytest.mark.asyncio
async def test_parent(app: App):
    """测试父插件"""
    from nonebot import require

    require("tests.plugins.nested")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help list")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件列表：\n帮助 # 获取插件帮助信息\n测试 # 一个测试插件", True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_sub(app: App):
    """测试子插件"""
    from nonebot import require

    require("tests.plugins.nested")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help 测试")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "测试\n\n功能一 # 测试插件子插件一\n功能二 # 测试插件子插件二", True)
        ctx.should_finished()
