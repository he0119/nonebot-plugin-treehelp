import pytest
from nonebug.app import App


@pytest.fixture
def app(nonebug_init: None, monkeypatch: pytest.MonkeyPatch) -> App:
    import nonebot

    # 加载插件
    nonebot.load_plugin("nonebot_plugin_treehelp")

    return App(monkeypatch)
