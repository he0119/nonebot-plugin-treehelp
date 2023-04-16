from nonebug import App

from .utils import make_fake_event, make_fake_message


async def test_help(app: App):
    """测试帮助"""
    from nonebot_plugin_treehelp import __plugin_meta__, help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, f"插件：\n帮助 # 获取插件帮助信息", True)
        ctx.should_finished()


async def test_help_help(app: App):
    """测试获取帮助插件帮助"""
    from nonebot_plugin_treehelp import __plugin_meta__, help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help 帮助")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            f"帮助\n\n{__plugin_meta__.usage}",
            True,
        )
        ctx.should_finished()


async def test_help_not_found(app: App):
    """测试插件不存在"""
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help test")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "未找到插件 test", True)
        ctx.should_finished()


async def test_help_command_error(app: App):
    """测试命令错误"""
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help --test")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            "usage: 帮助 [-h] [-t] [插件名]\n帮助: error: unrecognized arguments: --test\n",
            True,
        )
        ctx.should_finished()


async def test_help_by_command(app: App):
    """测试通过命令获取帮助信息"""
    from nonebot import require

    require("tests.plugins.tree")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help simple")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "简单功能\n\n/简单功能", True)
        ctx.should_finished()

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help simple.alias")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "简单功能\n\n/简单功能", True)
        ctx.should_finished()

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help sub")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "复杂功能\n\n/复杂功能\n\n二级功能 # 测试插件二级插件", True)
        ctx.should_finished()

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help sub.alias")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "复杂功能\n\n/复杂功能\n\n二级功能 # 测试插件二级插件", True)
        ctx.should_finished()

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help sub。alias")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "复杂功能\n\n/复杂功能\n\n二级功能 # 测试插件二级插件", True)
        ctx.should_finished()
