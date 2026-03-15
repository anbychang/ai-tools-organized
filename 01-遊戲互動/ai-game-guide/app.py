import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 遊戲攻略", page_icon="🎮")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    spoiler_level = st.select_slider(
        "🔒 劇透程度",
        options=["完全不劇透", "輕微提示", "中度提示", "詳細攻略"],
        value="輕微提示",
    )
    st.markdown("🔑 請先取得 [Groq API Key](https://console.groq.com/)")

st.title("🎮 AI 遊戲攻略助手")
st.markdown("卡關了嗎？告訴 AI 你在玩什麼遊戲、卡在哪裡，讓它給你策略提示！")

# --- 輸入 ---
game_name = st.text_input("🎮 遊戲名稱", placeholder="例如：薩爾達傳說：王國之淚")
stuck_desc = st.text_area(
    "😫 卡關描述",
    placeholder="例如：我在火焰神殿的第三層，有一個巨大的石門打不開，旁邊有兩個火把...",
    height=120,
)

# --- 額外選項 ---
col1, col2 = st.columns(2)
with col1:
    game_type = st.selectbox("遊戲類型", [
        "動作冒險", "角色扮演", "解謎", "射擊", "策略",
        "格鬥", "運動", "模擬", "其他",
    ])
with col2:
    platform = st.selectbox("遊戲平台", [
        "PC", "PlayStation", "Xbox", "Nintendo Switch", "手機", "其他",
    ])

generate = st.button("💡 取得攻略提示", use_container_width=True)

if generate:
    if not api_key:
        st.warning("⚠️ 請先在側邊欄輸入 Groq API Key。")
        st.stop()
    if not game_name.strip() or not stuck_desc.strip():
        st.warning("⚠️ 請輸入遊戲名稱和卡關描述。")
        st.stop()

    spoiler_map = {
        "完全不劇透": "只給方向性的暗示，完全不透露劇情或具體解法",
        "輕微提示": "給出輕微的提示，引導玩家思考方向，不直接給答案",
        "中度提示": "給出較明確的步驟提示，但保留一些讓玩家自己探索的空間",
        "詳細攻略": "給出完整的解題步驟和策略，但盡量避免劇透主線劇情",
    }

    prompt = (
        f"你是一位資深遊戲攻略專家。\n"
        f"遊戲：{game_name}（{game_type}，{platform}）\n"
        f"卡關描述：{stuck_desc}\n"
        f"劇透程度：{spoiler_level}（{spoiler_map[spoiler_level]}）\n\n"
        f"請用繁體中文提供攻略協助，包含：\n"
        f"1. 📍 目前位置/進度判斷\n"
        f"2. 💡 策略提示（根據劇透程度調整詳細度）\n"
        f"3. ⚔️ 戰鬥/操作技巧（如適用）\n"
        f"4. 🎒 建議裝備或道具準備\n"
        f"5. ⚠️ 常見錯誤提醒\n\n"
        f"請嚴格遵守劇透程度設定。"
    )

    client = Groq(api_key=api_key)
    with st.spinner("🎮 AI 正在查閱攻略..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "你是資深遊戲攻略專家，用繁體中文提供遊戲攻略。"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=2048,
            )
            result = response.choices[0].message.content
            st.divider()
            st.subheader(f"💡 《{game_name}》攻略提示")
            st.info(f"🔒 劇透程度：{spoiler_level}")
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
