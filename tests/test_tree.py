from nonebug import App

from .utils import make_fake_event, make_fake_message


async def test_root(app: App):
    """测试帮助"""
    from nonebot import require

    require("tests.plugins.tree")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件：\n帮助 # 获取插件帮助信息\n测试 # 一个测试插件", True)
        ctx.should_finished()


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
        ctx.should_call_send(event, "测试\n\n复杂功能 # 测试插件复杂子插件\n简单功能 # 测试插件简单子插件", True)
        ctx.should_finished()


async def test_tree_view(app: App):
    """测试树形结构"""
    from nonebot import require

    require("tests.plugins.tree")
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help --tree")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            "插件：\n帮助 # 获取插件帮助信息\n测试 # 一个测试插件\n├── 复杂功能 # 测试插件复杂子插件\n│   └── 二级功能 # 测试插件二级插件\n└── 简单功能 # 测试插件简单子插件",
            True,
        )
        ctx.should_finished()

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help --tree 测试")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            "测试 # 一个测试插件\n├── 复杂功能 # 测试插件复杂子插件\n│   └── 二级功能 # 测试插件二级插件\n└── 简单功能 # 测试插件简单子插件",
            True,
        )
        ctx.should_finished()
