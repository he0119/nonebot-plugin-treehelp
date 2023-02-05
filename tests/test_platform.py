from nonebug import App

from .utils import make_fake_event, make_fake_message


async def test_fake(app: App):
    """当没有指定 adapters 时，默认显示"""
    from nonebot import require

    require("tests.plugins.platform")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help list")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件列表：\n帮助 # 获取插件帮助信息\n适配器 # 测试不同适配器", True)
        ctx.should_finished()


async def test_fake_plugin(app: App):
    """测试 Fake 适配器"""
    from nonebot import require

    require("tests.plugins.platform")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help 适配器")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "适配器\n\nFake # 测试 Fake 适配器", True)
        ctx.should_finished()
