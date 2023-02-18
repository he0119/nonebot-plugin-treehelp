from nonebug import App

from .utils import make_fake_event, make_fake_message


async def test_adapters(app: App):
    """当没有指定 adapters 时，默认显示"""
    from nonebot import require

    require("tests.plugins.adapters")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help --list")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件：\n帮助 # 获取插件帮助信息\n适配器 # 测试不同适配器", True)
        ctx.should_finished()


async def test_adapters_plugin(app: App):
    """仅支持 Fake 适配器的插件"""
    from nonebot import require

    require("tests.plugins.adapters")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help 适配器")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "适配器\n\nFake # 测试 Fake 适配器", True)
        ctx.should_finished()


async def test_adapters_supported_plugin(app: App):
    """支持的插件"""
    from nonebot import require

    require("tests.plugins.adapters")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help Fake")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "Fake\n\n/fake", True)
        ctx.should_finished()


async def test_adapters_unsupported_plugin(app: App):
    """不支持的插件"""
    from nonebot import require

    require("tests.plugins.adapters")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help OneBot")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "未找到插件 OneBot", True)
        ctx.should_finished()
