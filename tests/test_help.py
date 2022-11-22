from nonebug import App

from .utils import make_fake_event, make_fake_message

#
# async def test_sort_commands(app: App):
#     from nonebot_plugin_treehelp.data_source import sort_commands

#     cmds = [
#         ("ff14", "nuannuan"),
#         ("时尚品鉴",),
#         ("最终幻想14", "时尚品鉴"),
#         ("nuannuan",),
#     ]
#     assert sort_commands(cmds) == [
#         ("ff14", "nuannuan"),
#         ("nuannuan",),
#         ("最终幻想14", "时尚品鉴"),
#         ("时尚品鉴",),
#     ]

#     cmds = [
#         ("时尚品鉴",),
#         ("最终幻想14", "时尚品鉴"),
#         ("nuannuan",),
#     ]
#     assert sort_commands(cmds) == [
#         ("nuannuan",),
#         ("最终幻想14", "时尚品鉴"),
#         ("时尚品鉴",),
#     ]


async def test_help(app: App):
    """测试帮助"""
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            "帮助\n\n获取插件列表\n/help list\n获取某个插件的帮助\n/help 插件名",
            True,
        )
        ctx.should_finished()


async def test_help_list(app: App):
    """测试查看所有插件"""
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help list")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "插件列表：\n帮助 # 获取插件帮助信息", True)
        ctx.should_finished()


async def test_help_help(app: App):
    """测试获取帮助插件帮助"""
    from nonebot_plugin_treehelp import help_cmd

    async with app.test_matcher(help_cmd) as ctx:
        bot = ctx.create_bot()
        message = message = make_fake_message()("/help 帮助")
        event = make_fake_event(_message=message)()

        ctx.receive_event(bot, event)
        ctx.should_call_send(
            event,
            "帮助\n\n获取插件列表\n/help list\n获取某个插件的帮助\n/help 插件名",
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
        ctx.should_call_send(event, "请输入支持的插件名", True)
        ctx.should_finished()
