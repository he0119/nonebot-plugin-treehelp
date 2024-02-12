import nonebot
import pytest
from nonebug import NONEBOT_INIT_KWARGS, App

from .utils import clear_plugins


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"command_sep": [".", "。"]}


@pytest.fixture(autouse=True)
def _register_adapters(nonebug_init: None):
    from nonebot import get_driver
    from nonebot.adapters.console import Adapter as ConsoleAdapter
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter
    from nonebot.adapters.onebot.v12 import Adapter as OnebotV12Adapter

    driver = get_driver()
    driver.register_adapter(ConsoleAdapter)
    driver.register_adapter(OnebotV11Adapter)
    driver.register_adapter(OnebotV12Adapter)


@pytest.fixture()
def app(nonebug_init: None):
    clear_plugins()
    # 加载插件
    nonebot.load_plugin("nonebot_plugin_treehelp")
    return App()
