import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 習慣追蹤", page_icon="🎯")
st.title("🎯 AI 習慣追蹤 — 21 天計畫")

with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("---")
    st.markdown("輸入你想養成的習慣，AI 為你設計 21 天計畫！")

if "habit_plan" not in st.session_state:
    st.session_state.habit_plan = ""
if "completed_days" not in st.session_state:
    st.session_state.completed_days = set()

st.subheader("🌱 習慣設定")
habit = st.text_input("想養成的習慣", placeholder="例如：每天運動 30 分鐘、早起、閱讀、冥想...")
motivation = st.text_input("你的動機", placeholder="為什麼想養成這個習慣？")

col1, col2 = st.columns(2)
with col1:
    difficulty = st.selectbox("目前難度感受", ["很難開始", "有點挑戰", "應該可以", "蠻有信心"])
with col2:
    time_slot = st.selectbox("偏好執行時段", ["早晨", "中午", "下午", "晚上", "彈性安排"])

if st.button("📋 產生 21 天計畫", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key。")
    elif not habit:
        st.warning("請輸入想養成的習慣。")
    else:
        client = Groq(api_key=api_key)
        prompt = f"""你是一位習慣養成教練。請為以下目標設計一個 21 天漸進式計畫。

目標習慣：{habit}
動機：{motivation if motivation else "未提供"}
難度感受：{difficulty}
偏好時段：{time_slot}

請用以下格式產生計畫（全部繁體中文）：

## 🎯 習慣目標：（一句話總結）

### 📅 第一週：建立基礎（第 1-7 天）
每天列出：
**Day X：**（每日迷你目標）💡（激勵小語）

### 📅 第二週：穩定成長（第 8-14 天）
同上格式

### 📅 第三週：鞏固習慣（第 15-21 天）
同上格式

### 🏆 里程碑獎勵
- 第 7 天完成：...
- 第 14 天完成：...
- 第 21 天完成：...

### 💪 遇到困難時的應對策略
（列出 3-5 個具體策略）

要求：
1. 每日目標要漸進式增加難度
2. 前幾天要非常簡單，降低門檻
3. 激勵小語要多樣化且真誠
4. 里程碑獎勵要具體且吸引人
5. 應對策略要實用"""

        with st.spinner("正在設計你的 21 天計畫..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=3000,
                )
                st.session_state.habit_plan = response.choices[0].message.content
                st.session_state.completed_days = set()
            except Exception as e:
                st.error(f"發生錯誤：{e}")

if st.session_state.habit_plan:
    st.markdown("---")

    # Progress tracker
    st.subheader("✅ 每日打卡")
    cols = st.columns(7)
    for day in range(1, 22):
        col_idx = (day - 1) % 7
        with cols[col_idx]:
            checked = st.checkbox(f"D{day}", value=(day in st.session_state.completed_days), key=f"day_{day}")
            if checked:
                st.session_state.completed_days.add(day)
            elif day in st.session_state.completed_days:
                st.session_state.completed_days.discard(day)

    done = len(st.session_state.completed_days)
    st.progress(done / 21, text=f"進度：{done}/21 天（{done * 100 // 21}%）")

    st.markdown("---")
    st.markdown(st.session_state.habit_plan)
    st.download_button(
        label="💾 下載計畫",
        data=st.session_state.habit_plan,
        file_name="21day_plan.txt",
        mime="text/plain",
    )
