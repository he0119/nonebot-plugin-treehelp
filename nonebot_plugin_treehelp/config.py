""" 配置 """
from typing import List

from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    treehelp_ignored_plugins: List[str] = []
    """需要忽略的插件"""


plugin_config = Config.parse_obj(get_driver().config)
