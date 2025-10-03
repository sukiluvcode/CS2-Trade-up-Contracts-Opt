from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ButtonList(BaseModel):
    """是否为当前饰品"""
    current: bool
    """饰品good_id"""
    id: int
    """磨损名称"""
    name: str
    """是否为切换类别的按钮"""
    switch: bool


class Container(BaseModel):
    """备注，包含大行动、稀有度、直售等信息"""
    comment: str
    """上线时间，指游戏内的更新上线时间"""
    created_at: str
    """收藏品id"""
    id: int
    """收藏品名称"""
    name: str
    """该武器箱当前价格"""
    price: Optional[float]
    """收藏品图片"""
    url: Optional[str]
    roi: Optional[float]


class Dpl(BaseModel):
    """buff求购价"""
    buff_buy_price: Optional[float]
    """buff在售价"""
    buff_sell_price: Optional[float]
    """类型编号"""
    def_index: float
    """多普勒id"""
    key: float
    """中文名称"""
    label: str
    """皮肤编号"""
    paint_index: int
    """hash名称"""
    short_name_en: str
    """英文数值"""
    value: str


class GoodsInfo(BaseModel):
    id: int
    turnover_number: int
    turnover_avg_price: Optional[float]
    period_at: datetime
    buff_id: int
    yyyp_id: int
    name: str
    market_hash_name: str

    buff_sell_price: Optional[float]
    buff_buy_price: Optional[float]
    buff_sell_num: int
    buff_buy_num: int

    yyyp_sell_price: Optional[float]
    yyyp_lease_num: int
    yyyp_transfer_price: Optional[float]
    yyyp_lease_price: Optional[float]
    yyyp_long_lease_price: Optional[float]
    yyyp_lease_annual: Optional[float]
    yyyp_long_lease_annual: Optional[float]
    yyyp_sell_num: int
    yyyp_steam_price: Optional[float]
    yyyp_buy_num: int
    yyyp_buy_price: Optional[float]

    sell_price_rate_1: Optional[float]
    sell_price_rate_7: Optional[float]
    sell_price_rate_15: Optional[float]
    sell_price_rate_30: Optional[float]
    sell_price_rate_90: Optional[float]
    sell_price_rate_180: Optional[float]
    sell_price_rate_365: Optional[float]

    sell_price_1: Optional[float]
    sell_price_7: Optional[float]
    sell_price_15: Optional[float]
    sell_price_30: Optional[float]
    sell_price_90: Optional[float]
    sell_price_180: Optional[float]
    sell_price_365: Optional[float]

    yyyp_sell_price_1: Optional[float]
    yyyp_sell_price_7: Optional[float]
    yyyp_sell_price_15: Optional[float]
    yyyp_sell_price_30: Optional[float]
    yyyp_sell_price_90: Optional[float]
    yyyp_sell_price_180: Optional[float]
    yyyp_sell_price_365: Optional[float]

    yyyp_sell_price_rate_1: Optional[float]
    yyyp_sell_price_rate_7: Optional[float]
    yyyp_sell_price_rate_15: Optional[float]
    yyyp_sell_price_rate_30: Optional[float]
    yyyp_sell_price_rate_90: Optional[float]
    yyyp_sell_price_rate_180: Optional[float]
    yyyp_sell_price_rate_365: Optional[float]

    r8_sell_price: Optional[float]
    r8_sell_num: int

    steam_sell_price: Optional[float]
    steam_sell_num: int
    steam_buy_price: Optional[float]
    steam_buy_num: int

    steam_buff_buy_conversion: Optional[float]
    steam_buff_sell_conversion: Optional[float]
    buff_steam_buy_conversion: Optional[float]
    buff_steam_sell_conversion: Optional[float]

    type_localized_name: str
    statistic: int
    img: str
    updated_at: datetime
    rank_num: int
    rank_num_change: int
    def_index: int
    paint_index: int

    c5_sell_price: Optional[float]
    c5_sell_num: int
    c5_lease_price: Optional[float]
    c5_long_lease_price: Optional[float]

    min_float: Optional[float]
    max_float: Optional[float]

    rarity_localized_name: Optional[str]
    quality_localized_name: Optional[str]
    exterior_localized_name: Optional[str]
    group_hash_name: Optional[str]


class StatisticListDPL(BaseModel):
    """饰品类型名称"""
    name: str
    """存世量"""
    statistic: float
    """最近统计日期"""
    statistic_at: str

class StatisticList(BaseModel):
    """饰品类型名称"""
    name: str
    """存世量"""
    statistic: float
    """最近统计日期"""
    statistic_at: str
    id: int
    exterior_localized_name: Optional[str]
    quality_localized_name: Optional[str]
    rarity_localized_name: Optional[str]

class Data(BaseModel):
    """响应数据"""
    """按钮列表，同类饰品不同磨损类型的切换列表"""
    button_list: List[ButtonList]
    """该饰品所属武器箱/收藏品"""
    container: List[Container]
    """多普勒列表"""
    dpl: List[Dpl]
    """饰品信息"""
    goods_info: GoodsInfo
    """废弃"""
    is_collection: List[str]
    """存世量列表，存储同类型的不同饰品的存世量"""
    statistic_list: List[StatisticList | StatisticListDPL]


class Info(BaseModel):
    """响应状态码"""
    code: int
    """响应数据"""
    data: Data
    """响应信息"""
    msg: str
