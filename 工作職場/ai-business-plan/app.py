import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 商業企劃產生器", page_icon="💡")

st.title("💡 AI 商業企劃產生器")
st.markdown("輸入你的創業想法，AI 幫你產生完整的商業企劃大綱。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 商業企劃核心要素")
    st.markdown(
        "- 問題與痛點\n"
        "- 解決方案\n"
        "- 目標市場\n"
        "- 商業模式\n"
        "- 競爭優勢"
    )

# --- 主要輸入 ---
idea = st.text_area(
    "💭 你的創業想法",
    placeholder="例如：開發一個 AI 驅動的寵物健康管理 APP，讓飼主可以追蹤寵物的飲食、運動與健康狀況...",
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    industry = st.selectbox(
        "🏭 產業類別",
        ["科技", "餐飲", "零售", "教育", "醫療健康", "金融", "娛樂",
         "旅遊", "物流", "農業", "製造", "其他"],
    )
with col2:
    stage = st.selectbox(
        "📊 目前階段",
        ["純粹想法", "已有初步研究", "已有原型/MVP", "已有少量客戶"],
    )

target = st.text_input("🎯 預期目標客群（選填）", placeholder="例如：25-40 歲的寵物飼主")
budget = st.selectbox(
    "💰 預估初期資金",
    ["10 萬以下", "10-50 萬", "50-100 萬", "100-500 萬", "500 萬以上", "尚未評估"],
)

# --- 產生企劃 ---
if st.button("🚀 產生商業企劃", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not idea:
        st.error("請輸入你的創業想法。")
    else:
        prompt = (
            f"你是一位經驗豐富的創業顧問與商業分析師。請根據以下創業想法，產生一份完整的商業企劃大綱。\n\n"
            f"創業想法：{idea}\n"
            f"產業類別：{industry}\n"
            f"目前階段：{stage}\n"
            f"目標客群：{target if target else '待定義'}\n"
            f"預估資金：{budget}\n\n"
            f"請用繁體中文，涵蓋以下重點：\n"
            f"1. **問題定義**：市場上存在什麼痛點？\n"
            f"2. **解決方案**：你的產品/服務如何解決？\n"
            f"3. **目標市場**：市場規模、客群特徵\n"
            f"4. **商業模式**：如何賺錢？收入來源？\n"
            f"5. **競爭優勢**：與競品相比的獨特之處\n"
            f"6. **行銷策略**：如何觸及目標客群？\n"
            f"7. **財務規劃**：初步成本估算與獲利時間軸\n"
            f"8. **風險評估**：主要風險與因應策略\n"
            f"9. **下一步行動**：立即可以做的 3 件事"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在分析你的創業想法..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的創業顧問，擅長商業分析與企劃撰寫。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=4096,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📋 商業企劃大綱")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
