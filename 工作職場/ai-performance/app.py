import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 績效自評產生器", page_icon="📈")

st.title("📈 AI 績效自評產生器")
st.markdown("輸入工作內容、成就與目標，AI 幫你撰寫績效考核自評文字。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 績效自評撰寫技巧")
    st.markdown(
        "- 用數據佐證成果\n"
        "- 強調影響力與貢獻\n"
        "- 展現成長與學習\n"
        "- 提出明確未來目標\n"
        "- 保持正面但務實"
    )

# --- 主要輸入 ---
col1, col2 = st.columns(2)
with col1:
    position = st.text_input("💼 你的職稱", placeholder="例如：資深產品經理")
with col2:
    department = st.text_input("🏢 部門", placeholder="例如：產品開發部")

period = st.selectbox(
    "📅 考核期間",
    ["上半年度", "下半年度", "全年度", "Q1", "Q2", "Q3", "Q4"],
)

responsibilities = st.text_area(
    "📋 主要工作內容",
    placeholder="列出你這段期間的主要工作職責與負責項目...",
    height=100,
)

achievements = st.text_area(
    "🏆 具體成就與成果",
    placeholder="例如：帶領團隊完成 X 專案，營收成長 30%；優化流程節省 20% 時間...",
    height=100,
)

goals = st.text_area(
    "🎯 下一期目標規劃",
    placeholder="例如：學習新技術、帶領更大團隊、提升客戶滿意度...",
    height=80,
)

style = st.selectbox(
    "🎭 撰寫風格",
    ["專業正式", "簡潔有力", "詳細完整", "謙虛務實"],
)

rating = st.selectbox(
    "⭐ 你認為的自我評分",
    ["優異（超越期望）", "良好（達成期望）", "尚可（部分達成）", "不指定"],
)

# --- 產生自評 ---
if st.button("📝 產生績效自評", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not responsibilities or not achievements:
        st.error("請填寫工作內容與具體成就。")
    else:
        prompt = (
            f"你是一位資深人資顧問，擅長協助員工撰寫績效自評。請根據以下資訊，產生專業的績效考核自評文字。\n\n"
            f"職稱：{position if position else '未提供'}\n"
            f"部門：{department if department else '未提供'}\n"
            f"考核期間：{period}\n"
            f"主要工作內容：{responsibilities}\n"
            f"具體成就：{achievements}\n"
            f"下期目標：{goals if goals else '未提供'}\n"
            f"撰寫風格：{style}\n"
            f"自我評分傾向：{rating}\n\n"
            f"請用繁體中文撰寫，包含以下段落：\n"
            f"1. **工作概述**：簡述本期主要工作範疇\n"
            f"2. **關鍵成果**：量化並強調具體成就\n"
            f"3. **能力展現**：展示的核心能力與成長\n"
            f"4. **挑戰與學習**：遇到的困難及如何克服\n"
            f"5. **未來規劃**：下一期的目標與自我提升計畫\n"
            f"6. **總結**：一段精煉的自我總評"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在撰寫績效自評..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是資深人資顧問，擅長績效管理與自評撰寫。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=3072,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📄 績效自評")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
