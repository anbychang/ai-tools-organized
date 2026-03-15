import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 殺價助手", page_icon="💰")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_bargain(product, original_price, target_price, scene, extra):
    """呼叫 Groq API 產生殺價策略"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位殺價談判專家，熟悉各種議價技巧。請根據以下資訊，提供殺價策略：

- 商品名稱：{product}
- 原價/開價：{original_price} 元
- 目標價格：{target_price} 元
- 購買場景：{scene}
- 補充說明：{extra if extra else '無'}

請提供：
1. 殺價策略分析（成功率評估、合理價格區間）
2. 開場白建議（怎麼開口議價）
3. 三段式殺價對話範例（買家 vs 賣家的完整對話模擬）
4. 進階談判技巧（至少 3 個實用技巧）
5. 如果賣家不讓步的替代方案

要求：
- 策略要實際可行
- 對話要自然不尷尬
- 考慮台灣的購物文化
- 既要殺到好價格，又不要讓場面太難看

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content


# 主頁面
st.title("💰 AI 殺價助手")
st.markdown("買東西想省錢？讓 AI 教你殺價的藝術！")

st.markdown("---")

product = st.text_input("商品名稱", placeholder="例如：iPhone 16 Pro、二手車、夜市皮包...")

col1, col2 = st.columns(2)
with col1:
    original_price = st.number_input("原價/開價（元）", min_value=1, value=10000, step=100)
with col2:
    target_price = st.number_input("目標價格（元）", min_value=1, value=8000, step=100)

scene = st.selectbox("購買場景", [
    "實體店面", "網路購物（私訊賣家）", "夜市/市場",
    "二手交易平台", "汽車/機車行", "傢俱/家電賣場",
    "房屋租賃/買賣", "其他"
])

extra = st.text_area(
    "補充說明（選填）",
    placeholder="例如：這是展示品、有小瑕疵、我想買多件...",
    height=80,
)

if st.button("🎯 產生殺價策略", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not product:
        st.warning("請輸入商品名稱！")
    elif target_price >= original_price:
        st.warning("目標價格應該低於原價！")
    else:
        with st.spinner("AI 正在分析殺價策略..."):
            try:
                result = generate_bargain(product, original_price, target_price, scene, extra)
                st.markdown("### 🎯 殺價攻略")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
