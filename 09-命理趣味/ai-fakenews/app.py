import json
import streamlit as st
try:
    from groq import Groq
except ImportError:
    Groq = None
from data.news_patterns import run_precheck

# ─── 頁面設定 ───
st.set_page_config(
    page_title="AI 假新聞偵測器",
    page_icon="🔍",
    layout="wide",
)

# ─── 自訂 CSS ───
st.markdown("""
<style>
    .score-high   { background: linear-gradient(90deg, #22c55e 0%, #16a34a 100%); }
    .score-medium { background: linear-gradient(90deg, #eab308 0%, #f59e0b 100%); }
    .score-low    { background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%); }
    .score-bar {
        height: 32px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 16px;
        margin: 8px 0;
    }
    .red-flag-item {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 8px 8px 0;
    }
    .suggestion-item {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 8px 8px 0;
    }
    .precheck-hit {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 8px 12px;
        margin: 4px 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── 快速測試範例 ───
EXAMPLES = {
    "範例 1：正常新聞（台積電）": (
        "台積電今日宣布將在高雄設立新的先進封裝廠，預計投資金額超過新台幣 300 億元，"
        "可望創造超過 3,000 個工作機會。經濟部表示，此投資案將有助於南台灣半導體產業聚落的發展。"
        "台積電董事長在記者會上指出，新廠預計 2027 年開始量產。"
    ),
    "範例 2：可疑新聞（健康謠言）": (
        "震驚！台大醫院不敢公開的秘密：每天喝這種水竟然能根治癌症！"
        "一位神秘的中醫師透露了祖傳秘方，西醫不敢說的驚人療效，"
        "99%的人不知道，趕快分享給你的家人！再不看就來不及了！"
    ),
    "範例 3：假新聞風格（政治操控）": (
        "獨家內幕！政府不想讓你知道的真相：據內部人士透露，"
        "某高官已經秘密將數千億資產轉移海外，全民都被騙了！"
        "這個賣國賊的無恥行為令人髮指，人神共憤！"
        "消息人士指出更多驚天醜聞即將曝光，轉瘋了！"
    ),
    "範例 4：正常新聞（氣象）": (
        "中央氣象署今日發布天氣預報，受東北季風影響，北部及東北部地區明日氣溫將下降至 15 度左右，"
        "並有局部短暫陣雨。氣象署提醒民眾注意保暖，山區可能有較大雨勢。"
        "預計此波冷空氣將持續至週四，週五起氣溫回升。"
    ),
}

# ─── 側邊欄 ───
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="輸入你的 Groq API Key...",
        help="前往 https://console.groq.com 取得免費 API Key",
    )
    st.divider()
    st.subheader("📌 快速測試範例")
    st.caption("點選下方按鈕，自動填入範例新聞內容進行測試。")

    for label in EXAMPLES:
        if st.button(label, use_container_width=True):
            st.session_state["news_input"] = EXAMPLES[label]
            st.session_state["news_url"] = ""

    st.divider()
    st.markdown(
        "**模型：** `llama-3.3-70b-versatile`  \n"
        "**技術：** 規則預檢 + AI 深度分析"
    )

# ─── 主區域標題 ───
st.title("🔍 AI 假新聞偵測器")
st.caption("貼上新聞內容或標題，AI 幫你判斷是否為假新聞")

# ─── 輸入區 ───
news_text = st.text_area(
    "📰 新聞內容",
    value=st.session_state.get("news_input", ""),
    height=200,
    placeholder="在此貼上新聞文章或標題...",
)
news_url = st.text_input(
    "🔗 新聞來源網址（選填）",
    value=st.session_state.get("news_url", ""),
    placeholder="https://...",
)

analyze_btn = st.button("🚀 開始分析", type="primary", use_container_width=True)


# ─── 繪製可信度量表 ───
def render_credibility_meter(score: int):
    if score >= 70:
        css_class = "score-high"
        emoji = "✅"
    elif score >= 40:
        css_class = "score-medium"
        emoji = "⚠️"
    else:
        css_class = "score-low"
        emoji = "🚨"

    st.markdown(
        f'<div class="score-bar {css_class}" style="width:{score}%">'
        f"{emoji} {score} / 100"
        f"</div>",
        unsafe_allow_html=True,
    )


# ─── 顯示規則預檢結果 ───
def render_precheck(precheck: dict):
    if not precheck["matched_categories"]:
        st.success("規則預檢未發現明顯可疑模式。")
        return

    risk = precheck["total_score"]
    if risk >= 10:
        st.error(f"⚠️ 規則預檢風險分數：**{risk}**（高風險）")
    elif risk >= 5:
        st.warning(f"⚠️ 規則預檢風險分數：**{risk}**（中風險）")
    else:
        st.info(f"規則預檢風險分數：**{risk}**（低風險）")

    for cat in precheck["matched_categories"]:
        kw_list = "、".join(f"`{k}`" for k in cat["matched"])
        st.markdown(
            f'<div class="precheck-hit">'
            f'<b>{cat["category"]}</b>：{cat["description"]}<br>'
            f"命中關鍵字：{kw_list}"
            f"</div>",
            unsafe_allow_html=True,
        )


# ─── AI 分析 ───
def analyze_with_ai(text: str, url: str, precheck: dict) -> dict | None:
    precheck_summary = ""
    if precheck["matched_categories"]:
        items = []
        for cat in precheck["matched_categories"]:
            items.append(f"- {cat['category']}：命中 {', '.join(cat['matched'])}")
        precheck_summary = (
            "\n\n【規則預檢結果】\n" + "\n".join(items) +
            f"\n預檢風險分數：{precheck['total_score']}"
        )

    url_info = f"\n新聞來源網址：{url}" if url else ""

    prompt = f"""你是一位專業的假新聞偵測分析師。請分析以下新聞內容，判斷其可信度。

【新聞內容】
{text}
{url_info}
{precheck_summary}

請以 JSON 格式回覆，包含以下欄位：
- credibility_score: 0-100 的整數，100 表示完全可信，0 表示完全不可信
- verdict: 只能是「可信」、「可疑」、「假新聞」三者之一
- red_flags: 字串陣列，列出所有可疑之處（若無可疑則為空陣列）
- explanation: 詳細分析說明（繁體中文，200字以內）
- fact_check_suggestions: 字串陣列，建議的事實查核方式或可查證的來源

判斷標準：
1. 是否有明確可查證的消息來源
2. 用語是否客觀中立
3. 是否有邏輯矛盾或不合理之處
4. 是否使用情緒操控或聳動標題手法
5. 內容是否符合常識與專業知識

只回覆 JSON，不要加任何其他文字或 markdown 格式標記。"""

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content.strip()
    # 嘗試清除可能的 markdown 包裹
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    raw = raw.strip()

    return json.loads(raw)


# ─── 顯示 AI 分析結果 ───
def render_results(result: dict):
    score = result.get("credibility_score", 50)
    verdict = result.get("verdict", "未知")

    # 判定結果標題
    if verdict == "可信":
        st.success(f"## 判定結果：{verdict}")
    elif verdict == "可疑":
        st.warning(f"## 判定結果：{verdict}")
    else:
        st.error(f"## 判定結果：{verdict}")

    # 可信度量表
    st.subheader("可信度分數")
    render_credibility_meter(score)

    col1, col2 = st.columns(2)

    # 可疑之處
    with col1:
        st.subheader("🚩 可疑之處")
        flags = result.get("red_flags", [])
        if flags:
            for flag in flags:
                st.markdown(
                    f'<div class="red-flag-item">{flag}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("未發現明顯可疑之處。")

    # 事實查核建議
    with col2:
        st.subheader("💡 事實查核建議")
        suggestions = result.get("fact_check_suggestions", [])
        if suggestions:
            for sug in suggestions:
                st.markdown(
                    f'<div class="suggestion-item">{sug}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("無額外建議。")

    # 詳細說明
    st.subheader("📝 分析說明")
    st.write(result.get("explanation", "無"))


# ─── 執行分析 ───
if analyze_btn:
    if not news_text.strip():
        st.warning("請先輸入新聞內容。")
    else:
        # 規則預檢（不需要 API Key）
        st.subheader("📋 規則式預檢")
        precheck = run_precheck(news_text)
        render_precheck(precheck)

        st.divider()

        # AI 深度分析（需要 API Key）
        if Groq is None:
            st.info("未安裝 groq 套件，僅提供規則式預檢。請執行 `pip install groq` 以啟用 AI 分析。")
        elif not api_key:
            st.info("如需 AI 深度分析，請在側邊欄輸入 Groq API Key。")
        else:
            st.subheader("🤖 AI 深度分析")
            with st.spinner("AI 正在分析中，請稍候..."):
                try:
                    result = analyze_with_ai(news_text, news_url, precheck)
                    if result:
                        render_results(result)
                    else:
                        st.error("AI 回傳結果解析失敗，請重試。")
                except json.JSONDecodeError:
                    st.error("AI 回傳的格式無法解析，請重試。")
                except Exception as e:
                    st.error(f"分析過程發生錯誤：{e}")
