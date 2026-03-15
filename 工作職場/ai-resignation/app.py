import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 離職信產生器", page_icon="✉️")

st.title("✉️ AI 離職信產生器")
st.markdown("選擇離職原因、年資與語氣，AI 幫你撰寫專業的離職信。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 小提醒")
    st.markdown(
        "- 離職信應保持專業\n"
        "- 避免抱怨或負面用語\n"
        "- 記得感謝公司與同事\n"
        "- 提及交接配合意願"
    )

# --- 主要輸入 ---
col1, col2 = st.columns(2)

with col1:
    reason = st.selectbox(
        "📋 離職原因",
        ["個人生涯規劃", "家庭因素", "健康因素", "進修深造", "轉換跑道",
         "薪資待遇", "工作環境", "搬遷至外地", "創業", "其他"],
    )

with col2:
    years = st.selectbox(
        "📅 在職年資",
        ["未滿 1 年", "1-2 年", "2-3 年", "3-5 年", "5-10 年", "10 年以上"],
    )

col3, col4 = st.columns(2)

with col3:
    tone = st.selectbox(
        "🎭 語氣風格",
        ["正式專業", "溫暖感謝", "簡潔俐落", "誠懇真摯"],
    )

with col4:
    position = st.text_input("💼 你的職稱", placeholder="例如：資深工程師")

company = st.text_input("🏢 公司名稱", placeholder="例如：台灣科技股份有限公司")
supervisor = st.text_input("👤 主管稱呼", placeholder="例如：王經理")
last_day = st.text_input("📆 預計最後工作日", placeholder="例如：2024 年 3 月 31 日")
extra = st.text_area("📝 想特別提到的事（選填）", placeholder="例如：感謝某個專案的經驗...", height=80)

# --- 產生離職信 ---
if st.button("📝 產生離職信", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not company or not supervisor:
        st.error("請填寫公司名稱與主管稱呼。")
    else:
        prompt = (
            f"你是一位專業的職場寫作顧問。請根據以下資訊撰寫一封離職信。\n\n"
            f"公司名稱：{company}\n"
            f"主管稱呼：{supervisor}\n"
            f"職稱：{position if position else '未提供'}\n"
            f"在職年資：{years}\n"
            f"離職原因：{reason}\n"
            f"預計最後工作日：{last_day if last_day else '待定'}\n"
            f"語氣風格：{tone}\n"
            f"額外備註：{extra if extra else '無'}\n\n"
            f"請用繁體中文撰寫，格式為正式書信格式，包含：\n"
            f"- 開頭稱呼\n"
            f"- 表達離職意願\n"
            f"- 簡述原因（委婉得體）\n"
            f"- 感謝公司栽培\n"
            f"- 表達交接配合意願\n"
            f"- 結尾祝福\n"
            f"- 署名處"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在撰寫離職信..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的職場寫作顧問，擅長撰寫正式商業書信。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📄 離職信")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
