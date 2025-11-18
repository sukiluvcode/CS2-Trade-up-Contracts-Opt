import re

from pydantic import BaseModel

from cs2.data_model.response_model import Info
from cs2.scrape.cs2_terms import wear_value, value_to_wear


class Item(Info):
    tradable: bool


class Weapon(BaseModel):
    weapon_name: str
    hash_names: list[str]
    min_float: float
    max_float: float

wear_rank_p = re.compile(r'\s*\(([^)]*)\)\s*$')
def build_weapon_identity(mappings: dict):
    identity = {}
    for container_name, content in mappings.items():
        for rarity, items in content.items():
            items: list[Item]
            weapon = {}
            float_ranges = []
            for item in items:
                weapon_name = wear_rank_p.sub('', item.data.goods_info.market_hash_name).strip()
                if item.data.goods_info.min_float is None or item.data.goods_info.max_float is None:
                    wear_rank = wear_rank_p.search(item.data.goods_info.market_hash_name).group(1)
                    wear_range = wear_value.get(wear_rank)
                    item.data.goods_info.min_float = float(wear_range.split('-')[0])
                    item.data.goods_info.max_float = float(wear_range.split('-')[1])
                if weapon_name not in weapon:
                    weapon[weapon_name] = {
                        'hash_names': [item.data.goods_info.market_hash_name],
                        'min_float': item.data.goods_info.min_float,
                        'max_float': item.data.goods_info.max_float,
                        'float_ranges': [(item.data.goods_info.min_float, item.data.goods_info.max_float)]
                    }
                else:
                    weapon[weapon_name]['hash_names'].append(item.data.goods_info.market_hash_name)
                    weapon[weapon_name]['min_float'] = min(weapon[weapon_name]['min_float'], item.data.goods_info.min_float)
                    weapon[weapon_name]['max_float'] = max(weapon[weapon_name]['max_float'], item.data.goods_info.max_float)
                    weapon[weapon_name]['float_ranges'].append((item.data.goods_info.min_float, item.data.goods_info.max_float))
            for w, value in weapon.items():
                float_ranges = value['float_ranges']
                float_ranges.sort()
                is_continuous = all(
                    float_ranges[i][1] == float_ranges[i + 1][0]
                    for i in range(len(float_ranges) - 1)
                )
                if not is_continuous:
                    print(f"Float ranges for {w} in {container_name} are not continuous: {float_ranges}")
            weapon_list = [
                Weapon(
                    weapon_name=k,
                    hash_names=v['hash_names'],
                    min_float=v['min_float'],
                    max_float=v['max_float']
                ) for k, v in weapon.items()
            ]
            identity.setdefault(container_name, {})[rarity] = weapon_list
    return identity

def return_hash_name(weaopn_name: str, float_: float):
    for range_str, wear_rank in value_to_wear.items():
        min_f, max_f = map(float, range_str.split('-'))
        if min_f <= float_ <= max_f:
            return f"{weaopn_name} ({wear_rank})"


