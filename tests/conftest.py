import nonebot
import pytest
from nonebug import NONEBOT_INIT_KWARGS, App
from nonebug.app import App

from .utils import clear_plugins


def pytest_configure(config: pytest.Config) -> None:
    config.stash[NONEBOT_INIT_KWARGS] = {"command_sep": [".", "。"]}


@pytest.fixture
def app(nonebug_init: None):
    clear_plugins()
    # 加载插件
    nonebot.load_plugin("nonebot_plugin_treehelp")
    return App()
