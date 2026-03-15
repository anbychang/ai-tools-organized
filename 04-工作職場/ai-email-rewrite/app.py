import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 信件改寫", page_icon="✉️")
st.title("✉️ AI 信件改寫助手")
st.subheader("把口語化的文字變成專業得體的信件")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 貼上想改寫的文字\n3. 選擇正式程度\n4. 取得專業信件")

# 主要內容
casual_text = st.text_area(
    "📝 貼上你想改寫的文字",
    height=200,
    placeholder="例如：老闆，我下禮拜想請假三天去旅行，可以嗎？"
)

col1, col2 = st.columns(2)
with col1:
    formality = st.selectbox("🎯 正式程度", ["正式", "半正式", "客氣"])
    email_type = st.selectbox("📧 信件類型", ["請假信", "工作回報", "請求協助", "道歉信", "感謝信", "邀請信", "拒絕婉拒", "自我介紹", "其他"])
with col2:
    recipient = st.text_input("👤 收件人稱呼", placeholder="例如：王經理、陳老師、HR")
    sender = st.text_input("✍️ 署名", placeholder="例如：王小明")

tone_options = st.multiselect(
    "💬 語氣要求（可多選）",
    ["禮貌", "簡潔", "誠懇", "積極", "委婉", "專業"],
    default=["禮貌", "專業"]
)

if st.button("📨 改寫信件", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not casual_text.strip():
        st.warning("請先輸入要改寫的文字！")
    else:
        formality_desc = {
            "正式": "非常正式的商業書信格式，用詞嚴謹",
            "半正式": "半正式的語氣，親切但不失專業",
            "客氣": "客氣有禮但不過於拘謹的語氣"
        }

        prompt = f"""你是一位專業的商業書信撰寫專家。請將以下口語化的文字改寫成專業的信件。

原始文字：
---
{casual_text}
---

正式程度：{formality} - {formality_desc[formality]}
信件類型：{email_type}
收件人：{recipient if recipient else '未指定'}
署名：{sender if sender else '未指定'}
語氣要求：{'、'.join(tone_options)}

請用繁體中文回答，提供：

1. **📧 完整信件** - 包含主旨、稱呼、正文、結尾敬語、署名
2. **📌 信件主旨建議** - 3 個合適的 Email 主旨
3. **💡 用詞改善說明** - 列出你改了哪些地方以及為什麼

請確保信件流暢自然，不要太生硬。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在改寫信件..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5,
                    max_tokens=3000,
                )
            st.markdown("---")
            st.markdown("### 💼 改寫後的專業信件")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
