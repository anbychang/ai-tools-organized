import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 記帳分析", page_icon="💰")
st.title("💰 AI 記帳分析")
st.caption("貼上您的消費紀錄，AI 幫您分類分析、找出省錢空間")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 在文字框貼上消費紀錄\n"
        "3. 選擇分析時間範圍\n"
        "4. 點擊「分析消費」按鈕"
    )
    st.markdown("### 輸入格式建議")
    st.markdown(
        "任何格式皆可，例如：\n"
        "- 早餐 50 元\n"
        "- 3/1 超商 120\n"
        "- 計程車 250、午餐 100"
    )


def analyze_expenses(records: str, period: str, income: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的理財顧問。使用者會提供消費紀錄，"
                    "請以繁體中文進行以下分析：\n"
                    "1. 消費分類統計（食、衣、住、行、育、樂等）\n"
                    "2. 各類別佔比\n"
                    "3. 消費模式與習慣分析\n"
                    "4. 可以節省的項目與具體建議\n"
                    "5. 預算分配建議\n"
                    "請用表格和清單呈現，數字盡量精確。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"時間範圍：{period}\n"
                    f"月收入：{income if income else '未提供'}\n"
                    f"消費紀錄：\n{records}"
                ),
            },
        ],
        temperature=0.5,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
col1, col2 = st.columns(2)
with col1:
    period = st.selectbox("紀錄時間範圍", ["一天", "一週", "兩週", "一個月"])
with col2:
    income = st.text_input("月收入（選填）", placeholder="例如：45000")

records_input = st.text_area(
    "請貼上消費紀錄",
    height=250,
    placeholder=(
        "範例：\n"
        "早餐 蛋餅+豆漿 50\n"
        "午餐 便當 80\n"
        "飲料 珍奶 65\n"
        "晚餐 火鍋 350\n"
        "計程車 180\n"
        "Netflix 月費 390\n"
        "超商 零食飲料 120"
    ),
)

if st.button("分析消費", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not records_input.strip():
        st.warning("請輸入消費紀錄。")
    else:
        with st.spinner("AI 正在分析您的消費紀錄..."):
            try:
                result = analyze_expenses(records_input, period, income)
                st.markdown("---")
                st.subheader("📊 消費分析報告")
                st.markdown(result)
            except Exception as e:
                st.error(f"分析時發生錯誤：{e}")

st.markdown("---")
st.caption("💡 記帳是理財的第一步，持之以恆就能看見改變。")
