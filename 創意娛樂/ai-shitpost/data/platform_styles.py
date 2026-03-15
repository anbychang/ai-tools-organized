"""
平台風格定義與範例模式
Platform style descriptions and example patterns for Taiwanese social media.
"""

PLATFORM_STYLES = {
    "Dcard": {
        "name": "Dcard",
        "emoji": "💚",
        "style_name": "長文故事體",
        "description": "Dcard 的文章風格偏向長篇故事敘述，常以第一人稱娓娓道來，喜歡鋪陳情境、製造懸念，結尾常有反轉或感嘆。用語偏年輕大學生族群，會使用「我朋友（沒有要戰）」「更：感謝大家的回覆」等慣用語。",
        "tone_notes": [
            "以「我」開頭的故事敘述",
            "段落分明，適當換行增加可讀性",
            "結尾常有「更新」或「補充說明」",
            "標題常用「有沒有人跟我一樣...」「想問大家...」",
            "會加上看板分類如 [感情] [心情] [閒聊]",
        ],
        "example_patterns": [
            "事情是這樣的，那天我跟朋友去{地點}，結果...",
            "先說結論：{結論}。\n\n故事要從{時間}說起...",
            "更新在B5～\n\n原本只是想抱怨一下，沒想到這麼多人回覆...",
        ],
        "hashtag_style": "少用 hashtag，偏向在文末加上看板標籤",
        "max_length": "500-1500字",
    },
    "PTT": {
        "name": "PTT",
        "emoji": "🟦",
        "style_name": "鄉民用語",
        "description": "PTT 風格精簡直接，大量使用鄉民特有用語和梗，如「4%」「可撥」「嘻嘻」「幫高調」等。推文文化盛行，文章常故意留下讓人「推」或「噓」的空間。行文較為嗆辣直白。",
        "tone_notes": [
            "標題格式：[問卦] / [閒聊] / [爆卦] / [心得]",
            "開頭常用「如題」「小弟我」「肥宅我」",
            "大量使用 PTT 專屬用語",
            "結尾常放「有沒有八卦？」「有沒有卦？」",
            "善用「-----」分隔線",
        ],
        "example_patterns": [
            "如題\n小弟我今天{事件}\n有沒有{主題}的八卦？",
            "[問卦] 有沒有{主題}的卦？\n肥宅我剛剛{事件}，是不是搞錯了什麼...",
            "幫高調\n這件事情不推不行\n{內容}\n--\n※ 發信站: 批踢踢實業坊(ptt.cc)",
        ],
        "hashtag_style": "不使用 hashtag，PTT 沒有 hashtag 文化",
        "max_length": "100-500字",
    },
    "Instagram": {
        "name": "Instagram",
        "emoji": "📸",
        "style_name": "文青風",
        "description": "Instagram 台灣用戶偏好文青感性風格，文字搭配精美照片。常使用詩意短句、生活感悟，善用換行營造呼吸感。大量使用 emoji 和 hashtag，中英文混用是常態。",
        "tone_notes": [
            "短句為主，每句換行",
            "大量使用 emoji 穿插文字間",
            "中英文混搭（如 vibe、chill、aesthetic）",
            "文末放大量 hashtag",
            "語氣偏療癒、正能量或小確幸",
        ],
        "example_patterns": [
            "☀️ {感性開頭}\n\n有時候覺得\n生活就是要這樣\n{感悟}\n\n📍{地點}",
            "✨ 今天的小確幸 ✨\n\n{內容}\n\n好喜歡這樣的日子\nLife is beautiful 🌿",
            "🌙\n\n{深夜感性文}\n\n也許我們都需要\n對自己溫柔一點\n\n#日常 #生活紀錄",
        ],
        "hashtag_style": "大量 hashtag，中英文混用，通常 10-20 個",
        "max_length": "100-300字（不含 hashtag）",
    },
    "Twitter": {
        "name": "Twitter / X",
        "emoji": "🐦",
        "style_name": "短句嗆辣",
        "description": "Twitter (X) 台灣用戶風格極度精簡，一兩句話表達觀點，常帶有諷刺或幽默感。善用迷因梗、時事哏，語氣可以很嗆或很廢。推文常故意製造反差或荒謬感。",
        "tone_notes": [
            "極短句，通常 1-3 句",
            "語氣直接、嗆辣或反諷",
            "善用「...」製造停頓感",
            "常以一句話製造反差笑點",
            "會引用時事或流行迷因",
        ],
        "example_patterns": [
            "{嗆辣觀點}，不接受反駁。",
            "所以{荒謬事件}是正常的嗎...我以為只有我這樣",
            "{看似正經的開頭}\n\n才怪。",
        ],
        "hashtag_style": "少量 hashtag，1-3 個，通常是時事或迷因標籤",
        "max_length": "50-140字",
    },
    "Threads": {
        "name": "Threads",
        "emoji": "🔗",
        "style_name": "輕鬆碎念",
        "description": "Threads 台灣用戶風格介於 IG 和 Twitter 之間，偏向日常碎念、輕鬆分享。比 Twitter 更長一些，比 IG 更隨性。常有互動式問句，鼓勵留言討論。",
        "tone_notes": [
            "日常碎念風格，像在跟朋友聊天",
            "常用問句結尾引發互動",
            "比 Twitter 更溫和，比 IG 更隨意",
            "會分享生活小事或突發奇想",
            "適度使用 emoji，不過度",
        ],
        "example_patterns": [
            "剛剛{日常事件}，突然覺得{感想}\n\n有人也是這樣嗎？😂",
            "認真問\n{問題}\n\n我先說我的答案：{回答}",
            "今天的{主題}心得：\n\n{內容}\n\n你們覺得呢？留言跟我說 👇",
        ],
        "hashtag_style": "少量 hashtag，0-5 個，風格輕鬆",
        "max_length": "50-300字",
    },
}

MOOD_STYLES = {
    "抱怨": {
        "emoji": "😤",
        "description": "充滿怨氣但帶點幽默的抱怨風格",
        "tone": "不滿、無奈、碎碎念",
        "keywords": ["到底為什麼", "真的很無言", "我受不了", "有夠扯", "傻眼", "吐血"],
    },
    "炫耀": {
        "emoji": "😏",
        "description": "低調（或不低調）炫耀的風格",
        "tone": "得意、假裝不經意、凡爾賽",
        "keywords": ["不小心", "其實也還好", "沒什麼啦", "分享一下", "小小的", "隨便弄弄"],
    },
    "求助": {
        "emoji": "🆘",
        "description": "真心（或假裝）求助的風格",
        "tone": "無助、焦急、拜託",
        "keywords": ["急", "在線等", "有人知道嗎", "救命", "怎麼辦", "拜託"],
    },
    "搞笑": {
        "emoji": "🤣",
        "description": "刻意搞笑或自嘲的風格",
        "tone": "荒謬、自嘲、kuso",
        "keywords": ["笑死", "我到底", "有夠好笑", "神扯", "超ㄎㄧㄤ", "哈哈哈哈"],
    },
    "感性": {
        "emoji": "🥺",
        "description": "觸動情感的深夜文風格",
        "tone": "感傷、溫暖、回憶",
        "keywords": ["突然覺得", "好想", "那個時候", "原來", "謝謝", "珍惜"],
    },
    "厭世": {
        "emoji": "💀",
        "description": "對人生感到倦怠的厭世風格",
        "tone": "消極、躺平、佛系",
        "keywords": ["算了", "都可以", "無所謂", "累了", "躺平", "隨便", "活著好累"],
    },
}

ENGAGEMENT_LEVELS = {
    "低": {"emoji": "😶", "description": "可能只有媽媽會按讚", "color": "#9E9E9E"},
    "中": {"emoji": "👍", "description": "朋友圈會有反應", "color": "#2196F3"},
    "高": {"emoji": "🔥", "description": "有機會上熱門", "color": "#FF9800"},
    "爆": {"emoji": "💥", "description": "準備被瘋傳", "color": "#F44336"},
}
