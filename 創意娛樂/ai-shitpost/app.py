import streamlit as st
import json
import re
from groq import Groq
from data.platform_styles import PLATFORM_STYLES, MOOD_STYLES, ENGAGEMENT_LEVELS

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI 廢文產生器 🗑️",
    page_icon="🗑️",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS for fun colorful UI
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
/* ---------- gradient header ---------- */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem 2.5rem;
    border-radius: 1rem;
    margin-bottom: 1.5rem;
    color: white;
    text-align: center;
}
.main-header h1 { margin: 0; font-size: 2.6rem; }
.main-header p  { margin: .4rem 0 0; font-size: 1.15rem; opacity: .9; }

/* ---------- post cards ---------- */
.post-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
    border: 2px solid #e0e0e0;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 15px rgba(0,0,0,.06);
    transition: transform .15s, box-shadow .15s;
}
.post-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,.10);
}

/* ---------- engagement badges ---------- */
.engagement-badge {
    display: inline-block;
    padding: .35rem 1rem;
    border-radius: 2rem;
    font-weight: 700;
    font-size: .95rem;
    color: white;
}

/* ---------- hashtag chips ---------- */
.hashtag-chip {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    padding: .25rem .7rem;
    border-radius: 1rem;
    margin: .2rem;
    font-size: .85rem;
}

/* ---------- platform tag ---------- */
.platform-tag {
    display: inline-block;
    padding: .3rem .9rem;
    border-radius: .5rem;
    font-weight: 600;
    font-size: .9rem;
    margin-bottom: .6rem;
    color: white;
    background: #444;
}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
}
section[data-testid="stSidebar"] * {
    color: #e0e0e0 !important;
}

/* ---------- misc ---------- */
.style-note {
    background: #fffde7;
    border-left: 4px solid #ffd600;
    padding: .8rem 1rem;
    border-radius: 0 .5rem .5rem 0;
    margin-bottom: 1rem;
    font-size: .92rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="main-header">
    <h1>🗑️ AI 廢文產生器</h1>
    <p>一鍵產出台灣社群平台風格的病毒式廢文，讓你的貼文被瘋傳！</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🔑 API 設定")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="到 https://console.groq.com 申請免費 API Key",
    )

    st.markdown("---")
    st.markdown("## 📖 使用說明")
    st.markdown(
        """
1. 輸入你的 **Groq API Key**
2. 在主畫面填入你想發文的**主題**
3. 選擇**平台**和**心情**
4. 按下「產生廢文」按鈕
5. 等 AI 幫你生出 3 篇廢文！
6. 複製喜歡的貼文直接去發！
"""
    )

    st.markdown("---")
    st.markdown("## 🎭 平台風格一覽")
    for key, pdata in PLATFORM_STYLES.items():
        st.markdown(f"**{pdata['emoji']} {pdata['name']}** — {pdata['style_name']}")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; opacity:.5; font-size:.8rem;'>Made with 💜 & AI</div>",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Main form
# ---------------------------------------------------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    topic = st.text_area(
        "✏️ 你想發什麼文？",
        placeholder="例如：今天加班到凌晨三點結果老闆說做錯了要重來...",
        height=100,
    )

with col_right:
    platform_options = list(PLATFORM_STYLES.keys())
    platform = st.selectbox(
        "📱 選擇平台",
        platform_options,
        format_func=lambda x: f"{PLATFORM_STYLES[x]['emoji']} {PLATFORM_STYLES[x]['name']} — {PLATFORM_STYLES[x]['style_name']}",
    )

    mood_options = list(MOOD_STYLES.keys())
    mood = st.selectbox(
        "🎭 選擇心情",
        mood_options,
        format_func=lambda x: f"{MOOD_STYLES[x]['emoji']} {x} — {MOOD_STYLES[x]['tone']}",
    )

# Show selected platform style note
pdata = PLATFORM_STYLES[platform]
st.markdown(
    f"""<div class="style-note">
    <strong>{pdata['emoji']} {pdata['name']} 風格筆記：</strong> {pdata['description']}<br>
    <strong>建議長度：</strong>{pdata['max_length']}｜<strong>Hashtag：</strong>{pdata['hashtag_style']}
</div>""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Generate button
# ---------------------------------------------------------------------------
generate_clicked = st.button("🚀 產生廢文！", use_container_width=True, type="primary")


# ---------------------------------------------------------------------------
# Generation logic
# ---------------------------------------------------------------------------
def build_prompt(topic: str, platform: str, mood: str) -> str:
    p = PLATFORM_STYLES[platform]
    m = MOOD_STYLES[mood]

    tone_bullets = "\n".join(f"  - {t}" for t in p["tone_notes"])
    example_bullets = "\n".join(f"  - {e}" for e in p["example_patterns"])
    mood_keywords = "、".join(m["keywords"])

    return f"""你是一位專精台灣社群媒體文化的 AI 廢文大師。請根據以下條件產生 **3 篇不同風格變化** 的社群貼文。

## 主題
{topic}

## 平台：{p['name']}（{p['style_name']}）
風格說明：{p['description']}
寫作要點：
{tone_bullets}
範例模式：
{example_bullets}
建議長度：{p['max_length']}
Hashtag 風格：{p['hashtag_style']}

## 心情語氣：{mood}（{m['description']}）
語氣：{m['tone']}
可參考關鍵字：{mood_keywords}

## 輸出格式要求
請嚴格以 JSON 格式輸出，不要包含任何其他文字，只輸出 JSON：
```json
[
  {{
    "post_text": "完整的貼文內容（含換行、emoji 等）",
    "hashtags": ["hashtag1", "hashtag2"],
    "engagement": "低/中/高/爆",
    "variation_label": "這個變體的特色標籤（2-4字）"
  }},
  {{
    "post_text": "...",
    "hashtags": ["..."],
    "engagement": "...",
    "variation_label": "..."
  }},
  {{
    "post_text": "...",
    "hashtags": ["..."],
    "engagement": "...",
    "variation_label": "..."
  }}
]
```

注意：
- 每篇貼文要有不同的切入角度或風格變化
- 貼文內容要道地、自然，像真人寫的
- 善用該平台的特有用語和格式
- engagement 要合理評估（不要三篇都是「爆」）
- hashtags 要符合該平台的 hashtag 使用習慣
- 只輸出 JSON，不要有任何前後說明文字"""


def parse_response(text: str) -> list[dict]:
    """Try to extract JSON array from the model response."""
    # Try to find JSON array in the response
    # First, try direct parse
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)

    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Try to find array in text
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return []


def generate_posts(api_key: str, topic: str, platform: str, mood: str) -> list[dict]:
    client = Groq(api_key=api_key)
    prompt = build_prompt(topic, platform, mood)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "你是台灣社群媒體廢文產生器。你只會輸出 JSON 格式的內容，不會輸出任何其他文字。",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
        max_tokens=4096,
    )

    content = response.choices[0].message.content or ""
    return parse_response(content)


# ---------------------------------------------------------------------------
# Display results
# ---------------------------------------------------------------------------
if generate_clicked:
    if not api_key:
        st.error("⚠️ 請先在左邊側邊欄輸入 Groq API Key！")
    elif not topic.strip():
        st.error("⚠️ 請輸入你想發文的主題！")
    else:
        with st.spinner("🤖 AI 正在努力幫你寫廢文中..."):
            try:
                posts = generate_posts(api_key, topic, platform, mood)
            except Exception as e:
                st.error(f"❌ 產生失敗：{e}")
                posts = []

        if posts:
            st.markdown("---")
            st.markdown("## 📝 你的廢文出爐了！")

            for i, post in enumerate(posts):
                post_text = post.get("post_text", "（無內容）")
                hashtags = post.get("hashtags", [])
                engagement = post.get("engagement", "中")
                label = post.get("variation_label", f"變體 {i+1}")

                # Validate engagement level
                if engagement not in ENGAGEMENT_LEVELS:
                    engagement = "中"

                eng = ENGAGEMENT_LEVELS[engagement]

                st.markdown(
                    f"""<div class="post-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:.8rem;">
        <span class="platform-tag">{pdata['emoji']} {pdata['name']} · {label}</span>
        <span class="engagement-badge" style="background:{eng['color']}">
            {eng['emoji']} 預測互動：{engagement} — {eng['description']}
        </span>
    </div>
</div>""",
                    unsafe_allow_html=True,
                )

                # Post content in a text-friendly container
                st.markdown(f"**📄 貼文內容：**")
                st.text_area(
                    f"post_{i}",
                    value=post_text,
                    height=200,
                    label_visibility="collapsed",
                    key=f"post_text_{i}",
                )

                # Copy button
                col_copy, col_hashtags = st.columns([1, 3])
                with col_copy:
                    # Use st.code for easy copy or a JS-based copy button
                    copy_text = post_text
                    if hashtags:
                        copy_text += "\n\n" + " ".join(f"#{h}" for h in hashtags)

                    st.code(copy_text, language=None)

                with col_hashtags:
                    if hashtags:
                        chips_html = " ".join(
                            f'<span class="hashtag-chip">#{h}</span>' for h in hashtags
                        )
                        st.markdown(
                            f"**🏷️ 建議 Hashtags：**<br>{chips_html}",
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown("*此平台風格不使用 hashtag*")

                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.warning("😅 AI 似乎沒有成功產出內容，請再試一次！")

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """<div style="text-align:center; opacity:.5; font-size:.85rem;">
    AI 廢文產生器 — 由 Groq + LLaMA 3.3 驅動 | 純屬娛樂，發文後果自負 😂
</div>""",
    unsafe_allow_html=True,
)
