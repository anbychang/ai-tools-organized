import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Excel 公式產生器", page_icon="📊")

st.title("📊 AI Excel 公式產生器")
st.markdown("用中文描述你的需求，AI 幫你寫出 Excel 公式並解釋運作原理。")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 常見需求範例")
    st.markdown(
        "- 根據條件加總某欄位\n"
        "- 查找並回傳對應的值\n"
        "- 計算兩個日期之間的天數\n"
        "- 從文字中擷取特定部分\n"
        "- 去除重複值"
    )

# --- 主要輸入 ---
description = st.text_area(
    "📝 描述你的需求",
    placeholder="例如：我想在 A 欄找到「已完成」的項目，然後把對應 B 欄的數字加總起來...",
    height=120,
)

col1, col2 = st.columns(2)
with col1:
    excel_version = st.selectbox(
        "📦 Excel 版本",
        ["Microsoft 365 / Excel 2021", "Excel 2019", "Excel 2016", "Google Sheets"],
    )
with col2:
    complexity = st.selectbox(
        "📊 複雜度偏好",
        ["簡單易懂優先", "效能最佳優先", "都可以"],
    )

data_desc = st.text_input(
    "📋 資料結構說明（選填）",
    placeholder="例如：A 欄是姓名、B 欄是部門、C 欄是銷售額...",
)

# --- 產生公式 ---
if st.button("⚡ 產生公式", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not description:
        st.error("請描述你的需求。")
    else:
        prompt = (
            f"你是一位 Excel 公式專家。請根據使用者的需求描述，提供正確的 Excel 公式。\n\n"
            f"使用者需求：{description}\n"
            f"Excel 版本：{excel_version}\n"
            f"複雜度偏好：{complexity}\n"
            f"資料結構：{data_desc if data_desc else '未特別說明'}\n\n"
            f"請用繁體中文回答，格式如下：\n"
            f"1. **公式**：提供完整的 Excel 公式（用程式碼區塊包起來）\n"
            f"2. **原理說明**：逐步解釋公式每個部分的功能\n"
            f"3. **使用步驟**：告訴使用者如何套用此公式\n"
            f"4. **注意事項**：可能需要注意的地方\n"
            f"5. **替代方案**：如果有其他寫法，也請提供\n\n"
            f"確保公式與指定的 Excel 版本相容。"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在撰寫公式..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是 Excel 公式專家，擅長用簡單的方式解釋複雜公式。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=2048,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📐 公式結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
