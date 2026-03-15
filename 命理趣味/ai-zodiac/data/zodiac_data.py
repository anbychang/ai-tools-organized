"""
十二星座資料庫
包含星座名稱、日期範圍、性格特質、元素屬性
"""

ZODIAC_SIGNS = [
    {
        "name": "牡羊座",
        "emoji": "♈",
        "element": "火象",
        "start_month": 3, "start_day": 21,
        "end_month": 4, "end_day": 19,
        "traits": "積極、熱情、勇敢、直率、衝動、領導力強",
        "description": "牡羊座是黃道十二宮的第一個星座，充滿活力與冒險精神，天生的領導者。"
    },
    {
        "name": "金牛座",
        "emoji": "♉",
        "element": "土象",
        "start_month": 4, "start_day": 20,
        "end_month": 5, "end_day": 20,
        "traits": "穩重、務實、耐心、固執、享受生活、重視安全感",
        "description": "金牛座踏實可靠，追求穩定與舒適的生活，對美食與藝術有獨到的品味。"
    },
    {
        "name": "雙子座",
        "emoji": "♊",
        "element": "風象",
        "start_month": 5, "start_day": 21,
        "end_month": 6, "end_day": 20,
        "traits": "聰明、善變、好奇、口才好、適應力強、多才多藝",
        "description": "雙子座思維敏捷，善於溝通交流，對新事物充滿好奇心與探索欲。"
    },
    {
        "name": "巨蟹座",
        "emoji": "♋",
        "element": "水象",
        "start_month": 6, "start_day": 21,
        "end_month": 7, "end_day": 22,
        "traits": "溫柔、體貼、念舊、情緒化、母性強、重視家庭",
        "description": "巨蟹座情感豐富，重視家庭與親密關係，有強烈的保護欲和同理心。"
    },
    {
        "name": "獅子座",
        "emoji": "♌",
        "element": "火象",
        "start_month": 7, "start_day": 23,
        "end_month": 8, "end_day": 22,
        "traits": "自信、大方、熱情、驕傲、有創造力、領袖氣質",
        "description": "獅子座天生自帶光環，慷慨大方，喜歡成為眾人焦點，有王者風範。"
    },
    {
        "name": "處女座",
        "emoji": "♍",
        "element": "土象",
        "start_month": 8, "start_day": 23,
        "end_month": 9, "end_day": 22,
        "traits": "細心、完美主義、分析力強、謙虛、挑剔、注重細節",
        "description": "處女座追求完美，注重細節與秩序，有卓越的分析能力和服務精神。"
    },
    {
        "name": "天秤座",
        "emoji": "♎",
        "element": "風象",
        "start_month": 9, "start_day": 23,
        "end_month": 10, "end_day": 22,
        "traits": "優雅、公正、社交能力強、猶豫不決、追求和諧、審美力佳",
        "description": "天秤座追求平衡與和諧，有優秀的社交能力和審美品味，重視公平正義。"
    },
    {
        "name": "天蠍座",
        "emoji": "♏",
        "element": "水象",
        "start_month": 10, "start_day": 23,
        "end_month": 11, "end_day": 21,
        "traits": "神秘、深情、意志力強、佔有欲強、洞察力敏銳、愛恨分明",
        "description": "天蠍座情感深沉而強烈，有敏銳的洞察力，對感情全心投入，極度忠誠。"
    },
    {
        "name": "射手座",
        "emoji": "♐",
        "element": "火象",
        "start_month": 11, "start_day": 22,
        "end_month": 12, "end_day": 21,
        "traits": "樂觀、自由、冒險、直言不諱、哲學思維、熱愛旅行",
        "description": "射手座熱愛自由與冒險，樂觀開朗，追求知識與真理，是天生的探險家。"
    },
    {
        "name": "摩羯座",
        "emoji": "♑",
        "element": "土象",
        "start_month": 12, "start_day": 22,
        "end_month": 1, "end_day": 19,
        "traits": "務實、有野心、自律、嚴謹、責任感強、堅韌不拔",
        "description": "摩羯座目標明確，腳踏實地，有強烈的責任感和事業心，是可靠的夥伴。"
    },
    {
        "name": "水瓶座",
        "emoji": "♒",
        "element": "風象",
        "start_month": 1, "start_day": 20,
        "end_month": 2, "end_day": 18,
        "traits": "獨立、創新、人道主義、叛逆、理性、重視友誼",
        "description": "水瓶座思想前衛獨立，有強烈的創新精神和人道主義理想，不拘泥於傳統。"
    },
    {
        "name": "雙魚座",
        "emoji": "♓",
        "element": "水象",
        "start_month": 2, "start_day": 19,
        "end_month": 3, "end_day": 20,
        "traits": "浪漫、直覺強、富有同情心、夢幻、藝術天賦、感性",
        "description": "雙魚座感性浪漫，富有想像力和同情心，有與生俱來的藝術天賦和靈性。"
    },
]

# 元素相性表
ELEMENT_COMPATIBILITY = {
    ("火象", "火象"): "高度相容，充滿激情與活力",
    ("火象", "土象"): "互補關係，火帶來動力，土提供穩定",
    ("火象", "風象"): "絕佳組合，風助火勢，相互激勵",
    ("火象", "水象"): "需要磨合，水火相激，但能產生蒸汽般的化學反應",
    ("土象", "土象"): "穩定踏實，共同建設美好未來",
    ("土象", "風象"): "差異較大，但可以互相學習成長",
    ("土象", "水象"): "自然和諧，水滋潤土地，土給水方向",
    ("風象", "風象"): "思想交流豐富，但可能缺乏落地感",
    ("風象", "水象"): "需要理解包容，風可能讓水起波瀾",
    ("水象", "水象"): "情感深厚，心靈相通，但要注意情緒管理",
}


def get_zodiac(month: int, day: int) -> dict:
    """根據月份和日期返回對應的星座資料"""
    for sign in ZODIAC_SIGNS:
        # 處理跨年星座（摩羯座：12/22 - 1/19）
        if sign["start_month"] > sign["end_month"]:
            if (month == sign["start_month"] and day >= sign["start_day"]) or \
               (month == sign["end_month"] and day <= sign["end_day"]):
                return sign
        else:
            if (month == sign["start_month"] and day >= sign["start_day"]) or \
               (month == sign["end_month"] and day <= sign["end_day"]) or \
               (sign["start_month"] < month < sign["end_month"]):
                return sign
    return ZODIAC_SIGNS[0]  # fallback


def get_element_compatibility(element_a: str, element_b: str) -> str:
    """取得兩個元素的相性描述"""
    key = (element_a, element_b)
    if key in ELEMENT_COMPATIBILITY:
        return ELEMENT_COMPATIBILITY[key]
    key_rev = (element_b, element_a)
    if key_rev in ELEMENT_COMPATIBILITY:
        return ELEMENT_COMPATIBILITY[key_rev]
    return "獨特的組合，充滿未知的可能性"
