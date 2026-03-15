import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 行程規劃", page_icon="✈️")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_itinerary(destination, days, budget, style, companions, extra):
    """呼叫 Groq API 產生行程規劃"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位專業的旅遊規劃師，熟悉世界各地的景點與旅遊資訊。請根據以下條件，規劃一份詳細的旅遊行程：

- 目的地：{destination}
- 旅遊天數：{days} 天
- 預算等級：{budget}
- 旅遊風格：{style}
- 同行者：{companions}
- 額外需求：{extra if extra else '無'}

請提供：
1. 逐日行程安排（每天的景點、活動、餐廳建議）
2. 每天的時間規劃（上午/下午/晚上）
3. 交通方式建議
4. 預估花費分配
5. 實用旅遊小提醒（天氣、注意事項、必帶物品）

要求：
- 行程節奏合理，不要太趕
- 包含當地特色體驗
- 考慮景點之間的交通距離
- 提供備案景點（如遇下雨）

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=3000,
    )
    return response.choices[0].message.content


# 主頁面
st.title("✈️ AI 行程規劃師")
st.markdown("告訴 AI 你想去哪裡，幫你規劃完美旅程！")

st.markdown("---")

destination = st.text_input("目的地", placeholder="例如：日本東京、泰國曼谷、台南、花蓮...")

col1, col2 = st.columns(2)
with col1:
    days = st.number_input("旅遊天數", min_value=1, max_value=30, value=3)
with col2:
    budget = st.selectbox("預算等級", [
        "省錢背包客", "小資輕旅行", "中等舒適", "豪華享受"
    ])

col3, col4 = st.columns(2)
with col3:
    style = st.selectbox("旅遊風格", [
        "文化歷史探索", "美食之旅", "自然風景",
        "購物血拼", "放鬆度假", "冒險刺激", "網美打卡", "親子同遊"
    ])
with col4:
    companions = st.selectbox("同行者", [
        "獨自旅行", "情侶/夫妻", "朋友團", "家庭旅遊", "帶長輩", "帶小孩"
    ])

extra = st.text_area(
    "額外需求（選填）",
    placeholder="例如：想看富士山、必吃拉麵、不想走太多路、有素食需求...",
    height=80,
)

if st.button("🗺️ 規劃行程", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not destination:
        st.warning("請輸入目的地！")
    else:
        with st.spinner("AI 正在為你規劃行程..."):
            try:
                result = generate_itinerary(destination, days, budget, style, companions, extra)
                st.markdown("### 🗺️ 你的專屬行程")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
