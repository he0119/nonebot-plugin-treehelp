import nonebot
import pytest
from nonebot import get_driver
from nonebot.adapters.console import Adapter as ConsoleAdapter
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter
from nonebot.adapters.onebot.v12 import Adapter as OnebotV12Adapter
from nonebug import NONEBOT_INIT_KWARGS, App
from pytest_asyncio import is_async_test

from .utils import clear_plugins


def pytest_collection_modifyitems(items: list[pytest.Item]):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"command_sep": [".", "。"]}


@pytest.fixture(scope="session", autouse=True)
async def after_nonebot_init(after_nonebot_init: None):
    # 加载适配器
    driver = get_driver()
    driver.register_adapter(ConsoleAdapter)
    driver.register_adapter(OnebotV11Adapter)
    driver.register_adapter(OnebotV12Adapter)


@pytest.fixture
def app(app: App):
    clear_plugins()
    # 加载插件
    nonebot.load_plugin("nonebot_plugin_treehelp")
    return app
