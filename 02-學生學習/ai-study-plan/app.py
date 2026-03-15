import streamlit as st
from groq import Groq
from datetime import date, timedelta

st.set_page_config(page_title="AI 讀書計畫", page_icon="📅")

# --- 側邊欄 ---
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("根據考試日期與科目，自動產生讀書計畫")

st.title("📅 AI 讀書計畫")
st.markdown("輸入考試資訊，AI 幫你規劃每日讀書進度。")

# --- 輸入區 ---
col1, col2 = st.columns(2)
with col1:
    exam_date = st.date_input("考試日期", value=date.today() + timedelta(days=14))
with col2:
    daily_hours = st.number_input("每日可讀書時數", min_value=0.5, max_value=16.0, value=4.0, step=0.5)

subjects = st.text_area(
    "考試科目（每行一科，可加備註）",
    height=150,
    placeholder="例如：\n數學（微積分第3-5章）\n物理（力學+熱學）\n英文（多益準備）",
)

difficulty = st.multiselect(
    "需要加強的科目（可多選）",
    options=[s.strip() for s in subjects.strip().split("\n") if s.strip()] if subjects.strip() else [],
)

def generate_plan(api_key: str, exam_date, subjects: str, daily_hours: float, difficulty: list) -> str:
    days_left = (exam_date - date.today()).days
    client = Groq(api_key=api_key)
    prompt = f"""你是一位專業的學習規劃師。請根據以下資訊，制定一份詳細的每日讀書計畫。

## 基本資訊
- 今天日期：{date.today()}
- 考試日期：{exam_date}
- 剩餘天數：{days_left} 天
- 每日可用時間：{daily_hours} 小時
- 考試科目：
{subjects}
- 需要加強的科目：{', '.join(difficulty) if difficulty else '無特別指定'}

## 要求
1. 請製作一份從今天到考試前一天的每日計畫表
2. 每天要標明日期、科目、讀書內容、時間分配
3. 需要加強的科目請分配較多時間
4. 考前最後 2-3 天安排總複習
5. 每週安排一次小測驗自我檢視
6. 請用表格格式呈現

請用繁體中文回覆。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是專業學習規劃師，擅長制定高效讀書計畫，請用繁體中文回覆。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return response.choices[0].message.content

# --- 產生按鈕 ---
if st.button("產生讀書計畫", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not subjects.strip():
        st.warning("請至少輸入一個考試科目。")
    elif exam_date <= date.today():
        st.error("考試日期必須在今天之後。")
    else:
        days_left = (exam_date - date.today()).days
        st.info(f"距離考試還有 **{days_left}** 天，每日可讀 **{daily_hours}** 小時")
        with st.spinner("AI 正在規劃你的讀書計畫..."):
            try:
                plan = generate_plan(api_key, exam_date, subjects, daily_hours, difficulty)
                st.markdown("---")
                st.subheader("你的專屬讀書計畫")
                st.markdown(plan)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
