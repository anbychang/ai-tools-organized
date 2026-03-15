import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 營養師", page_icon="🥗")
st.title("🥗 AI 營養師")
st.caption("輸入今日飲食，AI 為您分析營養狀況")

# 側邊欄設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入您的 Groq API Key")
    st.markdown("---")
    st.markdown("### 使用說明")
    st.markdown(
        "1. 輸入您的 Groq API Key\n"
        "2. 在文字框中輸入今日三餐內容\n"
        "3. 點擊「分析營養」按鈕\n"
        "4. AI 將提供完整營養分析"
    )


def analyze_meals(meals: str) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一位專業的營養師。使用者會提供今日的飲食內容，"
                    "請你進行以下分析並以繁體中文回覆：\n"
                    "1. 估算總熱量（大卡）\n"
                    "2. 蛋白質/碳水化合物/脂肪的比例\n"
                    "3. 可能缺乏的營養素\n"
                    "4. 改善建議\n"
                    "請用條理分明的格式回覆，適當使用表格或清單。"
                ),
            },
            {"role": "user", "content": f"以下是我今天的飲食內容：\n{meals}"},
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    return response.choices[0].message.content


# 主要介面
meals_input = st.text_area(
    "請輸入今日飲食內容",
    height=200,
    placeholder=(
        "範例：\n"
        "早餐：一杯豆漿、一個蛋餅\n"
        "午餐：排骨便當、一杯珍珠奶茶\n"
        "晚餐：滷肉飯、燙青菜、味噌湯\n"
        "點心：一包洋芋片"
    ),
)

if st.button("分析營養", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not meals_input.strip():
        st.warning("請輸入今日的飲食內容。")
    else:
        with st.spinner("AI 營養師正在分析您的飲食..."):
            try:
                result = analyze_meals(meals_input)
                st.markdown("---")
                st.subheader("📊 營養分析結果")
                st.markdown(result)
            except Exception as e:
                st.error(f"分析時發生錯誤：{e}")

st.markdown("---")
st.caption("⚠️ 本工具僅供參考，不能取代專業營養師的建議。")
