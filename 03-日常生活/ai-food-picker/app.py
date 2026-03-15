import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 叫外賣選擇器", page_icon="🍔")
st.title("🍔 AI 叫外賣選擇器")
st.subheader("不知道吃什麼？讓 AI 幫你決定！")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 設定心情與偏好\n3. 讓 AI 幫你決定！")

# 初始化 session state
if "pick_count" not in st.session_state:
    st.session_state.pick_count = 0

# 主要內容
col1, col2 = st.columns(2)
with col1:
    mood = st.selectbox("😊 現在的心情", ["開心", "疲憊", "壓力大", "無聊", "悲傷", "慶祝", "普通"])
    budget = st.selectbox("💰 預算（每人）", ["100 以下", "100-200", "200-400", "400-700", "700 以上（奢華一下）"])
with col2:
    people = st.selectbox("👥 用餐人數", ["1 人（自己吃）", "2 人", "3-4 人", "5 人以上"])
    meal_time = st.selectbox("⏰ 用餐時段", ["早餐", "午餐", "下午茶", "晚餐", "宵夜"])

flavor = st.multiselect(
    "🌶️ 口味偏好（可多選）",
    ["台式", "日式", "韓式", "中式", "泰式", "義式", "美式", "素食", "健康餐"],
    default=["台式"]
)

restrictions = st.text_input("🚫 不想吃的（選填）", placeholder="例如：不吃辣、不吃海鮮、不要便當...")

def generate_pick():
    st.session_state.pick_count += 1

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    pick_btn = st.button("🎯 幫我決定！", type="primary", use_container_width=True, on_click=generate_pick)
with col_btn2:
    repick_btn = st.button("🔄 再選一次", use_container_width=True, on_click=generate_pick)

if st.session_state.pick_count > 0:
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    else:
        is_repick = st.session_state.pick_count > 1
        prompt = f"""你是一位美食推薦專家。請根據以下條件，幫我決定今天要吃什麼外賣。
{'這是第 ' + str(st.session_state.pick_count) + ' 次選擇，請推薦跟之前不同的選項！' if is_repick else ''}

心情：{mood}
預算（每人）：{budget} 元
用餐人數：{people}
用餐時段：{meal_time}
口味偏好：{'、'.join(flavor)}
不想吃：{restrictions if restrictions else '無限制'}

請用繁體中文回答，提供：
1. **🏆 今天就吃這個！** - 給出一個明確的推薦（餐廳類型+具體餐點）
2. **📝 推薦原因** - 為什麼這個選擇適合現在的你
3. **🍽️ 推薦點餐組合** - 具體建議點什麼菜（含份量建議）
4. **💡 加點小建議** - 飲料或甜點搭配
5. **🔖 備選方案** - 再給 2 個備選選項

語氣請活潑有趣，像朋友在推薦一樣！"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在幫你挑選美食..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1.0,
                    max_tokens=2000,
                )
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
