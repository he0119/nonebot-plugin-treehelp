"""配置"""

from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    treehelp_ignored_plugins: list[str] = []
    """需要忽略的插件"""


plugin_config = get_plugin_config(Config)
