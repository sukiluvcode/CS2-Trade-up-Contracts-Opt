categories_str = \
"""
P2000
USP
格洛克
P250
FN57
CZ75
Tec-9
R8
沙漠之鹰
双持贝瑞塔
加利尔
SCAR-20
AWP
AK-47
法玛斯
M4A4
M4A1
SG 553
SSG 08
AUG
G3SG1
P90
MAC-10
UMP-45
MP7
PP-野牛
MP9
MP5-SD
截短霰弹枪
XM1014
新星
MAG-7
M249
内格夫
电击枪
"""

categories = categories_str.strip().split("\n")

rarity = """
消费级
工业级
军规级
受限
保密
隐秘
"""

wear_value = {
    'FN': '0.00-0.07',
    'MW': '0.07-0.15',
    'FT': '0.15-0.38',
    'WW': '0.38-0.45',
    'BS': '0.45-1.00',
}