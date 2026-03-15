import streamlit as st
from groq import Groq
import json

# --- 頁面設定 ---
st.set_page_config(page_title="AI 人生模擬器", page_icon="🎮", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("🎮 你的人生，你來選擇！")
    if st.button("🔄 重新開始人生"):
        for key in list(st.session_state.keys()):
            if key != "Groq API Key":
                del st.session_state[key]
        st.rerun()

# --- 初始化 session_state ---
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.round = 0
    st.session_state.happiness = 50
    st.session_state.wealth = 50
    st.session_state.health = 50
    st.session_state.history = []
    st.session_state.current_scenario = None
    st.session_state.age = 20

def display_stats():
    """顯示人生數值"""
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("😊 幸福", st.session_state.happiness)
    with c2:
        st.metric("💰 財富", st.session_state.wealth)
    with c3:
        st.metric("❤️ 健康", st.session_state.health)
    with c4:
        st.metric("🎂 年齡", st.session_state.age)
    # 數值條
    for label, val, color in [("幸福", st.session_state.happiness, "green"),
                               ("財富", st.session_state.wealth, "orange"),
                               ("健康", st.session_state.health, "red")]:
        st.progress(min(max(val, 0), 100) / 100, text=f"{label}: {val}/100")

def call_ai(prompt, system_msg):
    """呼叫 Groq AI"""
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
        temperature=0.9,
        max_tokens=1024,
    )
    return response.choices[0].message.content

# --- 主頁面 ---
st.title("🎮 AI 人生模擬器")

if not st.session_state.started:
    st.markdown("設定你的角色，開始模擬人生旅程！每個選擇都會影響你的人生數值。")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        start_age = st.number_input("🎂 起始年齡", min_value=18, max_value=60, value=22)
        career = st.selectbox("💼 職業", ["上班族", "學生", "自由工作者", "創業家", "藝術家", "工程師", "老師", "醫護人員"])
    with col2:
        location = st.selectbox("📍 居住地", ["台北", "台中", "高雄", "花蓮", "國外", "小鎮"])
        personality = st.selectbox("🧠 個性", ["冒險型", "穩健型", "社交型", "內向型", "理想主義"])

    if st.button("🚀 開始人生", type="primary", use_container_width=True):
        if not api_key:
            st.error("請在側邊欄輸入 Groq API Key！")
        else:
            st.session_state.started = True
            st.session_state.age = start_age
            st.session_state.career = career
            st.session_state.location = location
            st.session_state.personality = personality
            st.session_state.round = 1
            # 產生第一個情境
            try:
                prompt = f"""角色設定：{start_age}歲，職業：{career}，住在{location}，個性：{personality}
目前數值：幸福{st.session_state.happiness} 財富{st.session_state.wealth} 健康{st.session_state.health}

請產生一個人生情境和 3 個選擇。格式：
情境描述（2-3句生動描述）

選擇A：（描述）
選擇B：（描述）
選擇C：（描述）

情境要貼近現實生活，有趣且有意義。繁體中文。"""
                result = call_ai(prompt, "你是人生模擬器的敘事者，用繁體中文產生生動的人生情境和選擇。")
                st.session_state.current_scenario = result
                st.rerun()
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                st.session_state.started = False
else:
    display_stats()
    st.markdown("---")

    # 檢查遊戲結束
    if st.session_state.health <= 0 or st.session_state.age >= 100 or st.session_state.round > 15:
        st.subheader("🏁 人生旅程結束！")
        total = st.session_state.happiness + st.session_state.wealth + st.session_state.health
        st.markdown(f"**最終分數：{total}/300**")
        if total >= 200:
            st.success("🌟 精彩人生！你活出了令人羨慕的一生！")
        elif total >= 120:
            st.info("😊 還不錯的人生，有高有低，平凡而真實。")
        else:
            st.warning("😅 坎坷的人生，但每段經歷都是成長。")
        for i, h in enumerate(st.session_state.history):
            st.markdown(f"**第 {i+1} 回合（{h['age']}歲）：** {h['choice']}")
    elif st.session_state.current_scenario:
        st.subheader(f"📖 第 {st.session_state.round} 回合（{st.session_state.age} 歲）")
        st.markdown(st.session_state.current_scenario)
        st.markdown("---")

        choice = st.radio("你的選擇：", ["選擇A", "選擇B", "選擇C"], horizontal=True)

        if st.button("✅ 確認選擇", type="primary", use_container_width=True):
            if not api_key:
                st.error("請在側邊欄輸入 Groq API Key！")
            else:
                try:
                    prompt = f"""角色：{st.session_state.age}歲，{st.session_state.career}，住{st.session_state.location}
目前數值：幸福{st.session_state.happiness} 財富{st.session_state.wealth} 健康{st.session_state.health}
個性：{st.session_state.personality}

情境：{st.session_state.current_scenario}

玩家選擇了：{choice}

請提供：
1. 這個選擇的結果描述（2-3句）
2. 數值變化（格式必須嚴格為：幸福+X 財富+X 健康+X，X可以是正負數，範圍-20到+20）
3. 然後產生下一個新情境和 3 個新選擇（年齡增加2-5歲）

繁體中文回答。數值變化那行請用「數值變化：幸福+X 財富+X 健康+X」的格式。"""

                    with st.spinner("🎲 命運之輪轉動中..."):
                        result = call_ai(prompt, "你是人生模擬器敘事者，繁體中文。數值變化行格式：數值變化：幸福+X 財富+X 健康+X")

                    # 嘗試解析數值變化
                    import re
                    match = re.search(r'幸福([+-]?\d+)\s*財富([+-]?\d+)\s*健康([+-]?\d+)', result)
                    if match:
                        st.session_state.happiness = max(0, min(100, st.session_state.happiness + int(match.group(1))))
                        st.session_state.wealth = max(0, min(100, st.session_state.wealth + int(match.group(2))))
                        st.session_state.health = max(0, min(100, st.session_state.health + int(match.group(3))))

                    st.session_state.history.append({"age": st.session_state.age, "choice": choice})
                    st.session_state.age += 3
                    st.session_state.round += 1
                    st.session_state.current_scenario = result
                    st.rerun()

                except Exception as e:
                    st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("🎮 AI 人生模擬器 — 每個選擇都塑造你的人生故事")
