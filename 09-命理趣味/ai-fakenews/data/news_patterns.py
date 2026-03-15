"""
假新聞偵測 - 規則式預檢模式庫
包含聳動用語、點擊誘餌關鍵字、情緒操控詞彙等
"""

# 聳動用語 / 誇大標題常見詞
SENSATIONAL_KEYWORDS = [
    "震驚", "驚爆", "獨家", "內幕", "恐怖", "崩潰",
    "瘋傳", "嚇壞", "不敢相信", "太扯了", "傻眼",
    "全場驚呆", "史上最", "前所未見", "超狂", "炸裂",
    "毀三觀", "細思極恐", "令人髮指", "驚天", "爆料",
    "你絕對想不到", "看完都哭了", "轉瘋了", "99%的人不知道",
    "一夜之間", "全網瘋傳", "刪前速看", "官方不敢說",
]

# 點擊誘餌句型模式
CLICKBAIT_PATTERNS = [
    "你不知道的", "竟然是因為", "真相竟然是",
    "結局讓人", "看到最後", "第N個最",
    "一招解決", "只要這樣做", "醫生都推薦",
    "千萬不要", "趕快分享", "不轉不是",
    "快告訴你的家人", "再不看就來不及了",
    "政府不想讓你知道", "專家都沉默了",
    "背後的真相", "隱藏的秘密",
]

# 情緒操控用語
EMOTIONAL_MANIPULATION = [
    "憤怒", "痛心", "心寒", "無恥", "喪盡天良",
    "天理不容", "人神共憤", "令人作嘔", "噁心",
    "可惡至極", "滅絕人性", "罄竹難書", "禽獸不如",
    "血債血償", "忍無可忍", "是非不分", "黑白顛倒",
    "亡國滅種", "全民公敵", "賣國賊",
]

# 偽科學 / 健康謠言常見詞
PSEUDOSCIENCE_KEYWORDS = [
    "神奇療效", "一吃就好", "癌症剋星", "排毒",
    "秘方", "偏方", "祖傳", "西醫不敢說",
    "藥廠陰謀", "百病皆治", "永不復發", "根治",
    "驚人效果", "NASA認證", "諾貝爾認證",
    "量子", "磁場", "負離子", "鹼性體質",
]

# 假消息常見來源聲稱
FAKE_SOURCE_CLAIMS = [
    "據內部人士透露", "知情人士表示", "消息人士指出",
    "網友爆料", "有人說", "聽說", "據傳",
    "未經證實的消息", "小道消息",
]

# 所有模式的分類對應（用於報告）
PATTERN_CATEGORIES = {
    "sensational": {
        "name": "聳動用語",
        "keywords": SENSATIONAL_KEYWORDS,
        "weight": 2,
        "description": "使用誇大、聳動的詞彙吸引注意力",
    },
    "clickbait": {
        "name": "點擊誘餌",
        "keywords": CLICKBAIT_PATTERNS,
        "weight": 2,
        "description": "使用點擊誘餌式的句型引誘讀者",
    },
    "emotional": {
        "name": "情緒操控",
        "keywords": EMOTIONAL_MANIPULATION,
        "weight": 3,
        "description": "使用激烈情緒性用語操控讀者感受",
    },
    "pseudoscience": {
        "name": "偽科學用語",
        "keywords": PSEUDOSCIENCE_KEYWORDS,
        "weight": 3,
        "description": "包含偽科學或未經證實的健康宣稱",
    },
    "fake_source": {
        "name": "模糊消息來源",
        "keywords": FAKE_SOURCE_CLAIMS,
        "weight": 1,
        "description": "消息來源不明確或無法查證",
    },
}


def run_precheck(text: str) -> dict:
    """
    對輸入文本進行規則式預檢，回傳各類別的命中結果與初步風險分數。

    Returns:
        {
            "total_score": int,        # 風險分數 (越高越可疑)
            "matched_categories": [...] # 命中的類別與關鍵字
        }
    """
    results = []
    total_score = 0

    for cat_key, cat_info in PATTERN_CATEGORIES.items():
        matched_keywords = [kw for kw in cat_info["keywords"] if kw in text]
        if matched_keywords:
            score = len(matched_keywords) * cat_info["weight"]
            total_score += score
            results.append({
                "category": cat_info["name"],
                "description": cat_info["description"],
                "matched": matched_keywords,
                "score": score,
            })

    return {
        "total_score": total_score,
        "matched_categories": results,
    }
