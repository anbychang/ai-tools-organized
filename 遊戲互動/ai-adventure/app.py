import re
import streamlit as st
from groq import Groq

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI 文字冒險遊戲",
    page_icon="⚔️",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(170deg, #0d1117 0%, #161b22 50%, #1a1206 100%);
    }

    /* Adventure log container */
    .adventure-log {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.6rem;
        max-height: 520px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #58a6ff #161b22;
    }

    /* Individual message bubbles */
    .msg-dm {
        background: linear-gradient(135deg, #1c2333 0%, #1a1a2e 100%);
        border-left: 3px solid #f0a500;
        border-radius: 0 10px 10px 0;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
        color: #e6edf3;
        line-height: 1.7;
        font-size: 0.97rem;
    }

    .msg-player {
        background: linear-gradient(135deg, #0d2137 0%, #0a1929 100%);
        border-left: 3px solid #58a6ff;
        border-radius: 0 10px 10px 0;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.7rem;
        color: #79c0ff;
        line-height: 1.7;
        font-size: 0.97rem;
    }

    .msg-label {
        font-weight: 700;
        margin-bottom: 0.2rem;
        font-size: 0.82rem;
        letter-spacing: 0.5px;
    }

    .dm-label { color: #f0a500; }
    .player-label { color: #58a6ff; }

    /* Status bar */
    .status-bar {
        background: linear-gradient(90deg, #161b22 0%, #1c2333 100%);
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 0.7rem 1.2rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 0.4rem;
    }

    .stat-item {
        text-align: center;
        min-width: 80px;
    }

    .stat-value {
        font-size: 1.3rem;
        font-weight: 800;
        display: block;
    }

    .stat-label {
        font-size: 0.75rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .hp-color { color: #f85149; }
    .mp-color { color: #58a6ff; }
    .gold-color { color: #f0a500; }
    .class-color { color: #a5d6ff; }

    /* Title */
    .game-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #f0a500, #ff6b6b, #58a6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
        letter-spacing: 1px;
    }

    .game-subtitle {
        text-align: center;
        color: #8b949e;
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
    }

    /* Sidebar tweaks */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Character class definitions
# ---------------------------------------------------------------------------
CLASS_INFO = {
    "戰士": {"emoji": "🗡️", "hp": 120, "mp": 30, "desc": "近戰高手，血量充沛，擅長劍術與盾牌防禦。"},
    "法師": {"emoji": "🔮", "hp": 70, "mp": 120, "desc": "精通元素魔法，攻擊力驚人但身體脆弱。"},
    "盜賊": {"emoji": "🗝️", "hp": 90, "mp": 50, "desc": "敏捷靈活，擅長暗殺、開鎖與偵查陷阱。"},
    "弓箭手": {"emoji": "🏹", "hp": 85, "mp": 60, "desc": "遠程射擊專家，擁有銳利的鷹眼與追蹤技能。"},
}

# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
DEFAULTS = {
    "messages": [],       # conversation history sent to LLM
    "adventure_log": [],  # display log: list of (role, text)
    "hp": 100,
    "mp": 50,
    "gold": 0,
    "started": False,
    "character_class": "戰士",
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_game():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


# ---------------------------------------------------------------------------
# System prompt builder
# ---------------------------------------------------------------------------
def build_system_prompt(char_class: str) -> str:
    info = CLASS_INFO[char_class]
    return f"""你是一位極富創意的地下城主（Dungeon Master），正在主持一場沉浸式的繁體中文文字冒險RPG遊戲。

玩家資訊：
- 職業：{char_class} {info['emoji']}
- 初始 HP：{info['hp']}　MP：{info['mp']}　金幣：0

遊戲規則與風格：
1. 用生動、富有畫面感的繁體中文描述場景、角色與事件。
2. 每次回覆結尾提供 2-4 個行動選項讓玩家選擇（用數字列表）。
3. 追蹤玩家的 HP、MP、金幣。戰鬥或事件中合理扣除或增加。
4. 每次回覆最後一行必須用以下格式顯示狀態：
   【HP: X / {info['hp']} | MP: X / {info['mp']} | 金幣: X】
5. 讓故事有趣、充滿驚喜。適當加入戰鬥、謎題、NPC互動、隱藏寶藏。
6. 如果玩家 HP 歸零，宣布遊戲結束並提供重新開始的選項。
7. 玩家可以輸入任何自由行動，你需要合理判斷結果。
8. 回覆控制在 200-350 字以內，保持節奏明快。

現在，請以地下城主的身份開始一段全新的冒險故事吧！描述玩家在一個神秘的場景中醒來……"""


# ---------------------------------------------------------------------------
# Groq chat helper
# ---------------------------------------------------------------------------
def chat_with_groq(api_key: str, messages: list) -> str:
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.85,
        max_tokens=1024,
    )
    return resp.choices[0].message.content


def parse_status(text: str):
    """Try to extract HP / MP / Gold from the status line."""
    m = re.search(r"HP:\s*(\d+)", text)
    if m:
        st.session_state.hp = int(m.group(1))
    m = re.search(r"MP:\s*(\d+)", text)
    if m:
        st.session_state.mp = int(m.group(1))
    m = re.search(r"金幣:\s*(\d+)", text)
    if m:
        st.session_state.gold = int(m.group(1))


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")

    st.markdown("---")
    st.markdown("### 🎭 選擇職業")
    chosen_class = st.radio(
        "職業",
        list(CLASS_INFO.keys()),
        format_func=lambda c: f"{CLASS_INFO[c]['emoji']} {c}",
        label_visibility="collapsed",
    )
    if chosen_class:
        info = CLASS_INFO[chosen_class]
        st.caption(info["desc"])
        st.markdown(
            f"<small>HP <b>{info['hp']}</b> ｜ MP <b>{info['mp']}</b></small>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("🔄 開始新遊戲", use_container_width=True):
        reset_game()
        st.rerun()

    st.markdown("---")
    st.caption("Powered by Groq + LLaMA 3.3 70B")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.markdown('<div class="game-title">⚔️ AI 文字冒險遊戲</div>', unsafe_allow_html=True)
st.markdown('<div class="game-subtitle">由 AI 地下城主帶領你展開史詩冒險</div>', unsafe_allow_html=True)

# Status bar
info = CLASS_INFO.get(st.session_state.character_class, CLASS_INFO["戰士"])
max_hp = info["hp"]
max_mp = info["mp"]

st.markdown(
    f"""
    <div class="status-bar">
        <div class="stat-item">
            <span class="stat-value hp-color">❤️ {st.session_state.hp}/{max_hp}</span>
            <span class="stat-label">HP</span>
        </div>
        <div class="stat-item">
            <span class="stat-value mp-color">💧 {st.session_state.mp}/{max_mp}</span>
            <span class="stat-label">MP</span>
        </div>
        <div class="stat-item">
            <span class="stat-value gold-color">💰 {st.session_state.gold}</span>
            <span class="stat-label">金幣</span>
        </div>
        <div class="stat-item">
            <span class="stat-value class-color">{info['emoji']} {st.session_state.character_class}</span>
            <span class="stat-label">職業</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Start game automatically on first valid config
# ---------------------------------------------------------------------------
if not st.session_state.started and api_key:
    st.session_state.character_class = chosen_class
    info = CLASS_INFO[chosen_class]
    st.session_state.hp = info["hp"]
    st.session_state.mp = info["mp"]
    st.session_state.gold = 0

    system_msg = build_system_prompt(chosen_class)
    st.session_state.messages = [{"role": "system", "content": system_msg}]

    with st.spinner("地下城主正在創建冒險世界..."):
        try:
            reply = chat_with_groq(api_key, st.session_state.messages)
        except Exception as e:
            st.error(f"無法連線到 Groq API：{e}")
            st.session_state.messages = []
            st.stop()

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.adventure_log.append(("dm", reply))
    parse_status(reply)
    st.session_state.started = True
    st.rerun()

# ---------------------------------------------------------------------------
# Adventure log display
# ---------------------------------------------------------------------------
if st.session_state.adventure_log:
    log_html = ""
    for role, text in st.session_state.adventure_log:
        escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        if role == "dm":
            log_html += (
                f'<div class="msg-dm">'
                f'<div class="msg-label dm-label">🏰 地下城主</div>'
                f"{escaped}</div>"
            )
        else:
            log_html += (
                f'<div class="msg-player">'
                f'<div class="msg-label player-label">🧙 冒險者</div>'
                f"{escaped}</div>"
            )
    st.markdown(f'<div class="adventure-log">{log_html}</div>', unsafe_allow_html=True)
else:
    if not api_key:
        st.info("👈 請先在側邊欄輸入你的 Groq API Key，然後選擇職業即可開始冒險！")
    else:
        st.info("載入中...")

# ---------------------------------------------------------------------------
# Player input
# ---------------------------------------------------------------------------
if st.session_state.started:
    if not api_key:
        st.warning("⚠️ 請在側邊欄重新輸入你的 Groq API Key 以繼續冒險。")
    else:
        player_input = st.chat_input("輸入你的行動（例如：選擇 1、搜索房間、攻擊怪物...）")

        if player_input:
            # Add player message
            st.session_state.messages.append({"role": "user", "content": player_input})
            st.session_state.adventure_log.append(("player", player_input))

            # Get AI response
            with st.spinner("地下城主思考中..."):
                try:
                    reply = chat_with_groq(api_key, st.session_state.messages)
                except Exception as e:
                    st.error(f"API 呼叫失敗：{e}")
                    # Roll back the player message so it can be retried
                    st.session_state.messages.pop()
                    st.session_state.adventure_log.pop()
                    st.stop()

            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.adventure_log.append(("dm", reply))
            parse_status(reply)
            st.rerun()
