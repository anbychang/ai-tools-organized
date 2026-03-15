import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 會議摘要", page_icon="📝")
st.title("📝 AI 會議摘要助手")
st.subheader("貼上會議紀錄，AI 自動整理重點摘要")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    output_format = st.selectbox("📄 輸出格式", ["條列式", "表格式", "簡報重點"])
    language_style = st.selectbox("✍️ 語氣風格", ["正式商業", "簡潔明瞭", "詳細完整"])
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 貼上會議筆記\n3. 點擊產生摘要")

# 主要內容
meeting_notes = st.text_area(
    "📋 貼上會議紀錄或筆記",
    height=300,
    placeholder="在這裡貼上你的會議紀錄...\n\n可以是：\n- 逐字稿\n- 簡單筆記\n- 聊天記錄\n- 零散的重點"
)

col1, col2 = st.columns(2)
with col1:
    meeting_type = st.selectbox("🏷️ 會議類型", ["一般會議", "專案進度", "腦力激盪", "決策會議", "週會", "一對一", "客戶會議"])
with col2:
    meeting_date = st.date_input("📅 會議日期")

if st.button("🤖 產生會議摘要", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not meeting_notes.strip():
        st.warning("請先貼上會議紀錄！")
    else:
        prompt = f"""你是一位專業的會議記錄整理專家。請將以下會議紀錄整理成結構化的摘要。

會議類型：{meeting_type}
會議日期：{meeting_date}
輸出格式：{output_format}
語氣風格：{language_style}

會議紀錄內容：
---
{meeting_notes}
---

請用繁體中文回答，整理出以下內容：

1. **📌 會議主題與目的**
2. **🎯 關鍵決策** - 會議中做出的重要決定
3. **📋 待辦事項（Action Items）** - 用表格呈現：
   | 項目 | 負責人 | 截止日期 | 優先級 |
4. **💡 重要討論摘要** - 主要討論的議題與結論
5. **⚠️ 待確認事項** - 尚未確定或需要後續跟進的問題
6. **📅 下次會議** - 如果有提到的話

請確保不遺漏任何重要資訊，同時去除冗餘內容。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在整理會議摘要..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=4096,
                )
            st.markdown("---")
            st.markdown("### 📊 會議摘要")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
