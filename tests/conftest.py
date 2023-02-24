import nonebot
import pytest
from nonebug.app import App

from .utils import clear_plugins


@pytest.fixture
def app(nonebug_init: None):
    clear_plugins()
    # 加载插件
    nonebot.load_plugin("nonebot_plugin_treehelp")
    return App()
