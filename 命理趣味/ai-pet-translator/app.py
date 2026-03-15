import streamlit as st
from groq import Groq

# --- 頁面設定 ---
st.set_page_config(page_title="AI 寵物翻譯機", page_icon="🐾", layout="centered")

# --- 可愛風格 CSS ---
st.markdown("""
<style>
    .pet-bubble {
        background: linear-gradient(135deg, #fff3e0, #ffe0b2);
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        border: 2px solid #ffb74d;
        position: relative;
    }
    .pet-bubble::before {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 30px;
        border-width: 10px 10px 0;
        border-style: solid;
        border-color: #ffb74d transparent transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 **Llama 3.3 70B** 模型")
    st.markdown("🐾 終於能聽懂毛孩的心聲了！")

# --- 主頁面 ---
st.title("🐾 AI 寵物翻譯機")
st.markdown("選擇你的毛孩，描述牠的行為，AI 幫你翻譯牠在想什麼！")

col1, col2 = st.columns(2)
with col1:
    animal = st.selectbox("🐱 選擇動物", ["貓咪 🐱", "狗狗 🐶", "兔子 🐰", "倉鼠 🐹", "鸚鵡 🦜"])
with col2:
    pet_name = st.text_input("💝 毛孩名字", placeholder="例如：咪咪、旺財")

common_behaviors = {
    "貓咪 🐱": ["一直喵喵叫", "瘋狂甩尾巴", "躲在箱子裡", "磨蹭你的腳", "盯著牆壁看", "打翻東西", "露出肚子", "半夜暴衝"],
    "狗狗 🐶": ["一直汪汪叫", "瘋狂搖尾巴", "躲到桌子底下", "舔你的臉", "歪頭看你", "追自己尾巴", "趴在門口等", "拆家"],
    "兔子 🐰": ["跳來跳去", "磨牙", "舔你的手", "用後腳踏地", "躲在角落", "蹭你"],
    "倉鼠 🐹": ["跑滾輪", "藏食物", "咬籠子", "站起來看你", "挖洞", "洗臉"],
    "鸚鵡 🦜": ["一直叫", "學說話", "磨嘴", "張開翅膀", "低頭讓你摸", "咬人"],
}

behavior_options = common_behaviors.get(animal, ["其他行為"])
behavior = st.multiselect("🎭 選擇行為（可多選）", behavior_options)
extra_behavior = st.text_input("📝 其他行為補充", placeholder="描述更多細節...")
situation = st.text_input("📍 當時的情境", placeholder="例如：你剛到家、正在吃飯、半夜三點...")

if st.button("🔊 翻譯毛孩心聲", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not behavior and not extra_behavior.strip():
        st.error("請至少選擇一個行為或補充描述！")
    else:
        try:
            client = Groq(api_key=api_key)
            all_behaviors = ", ".join(behavior) + (f", {extra_behavior}" if extra_behavior.strip() else "")
            name_str = pet_name if pet_name.strip() else "這隻毛孩"
            prompt = f"""你是一位能與動物溝通的寵物翻譯師。請翻譯這隻寵物在想什麼。

動物類型：{animal}
名字：{name_str}
行為表現：{all_behaviors}
當時情境：{situation if situation.strip() else "日常"}

請提供：
1. 🗣️ 寵物的內心獨白（用第一人稱，口語化、可愛、有個性，200字左右）
2. 🧠 行為解讀（從動物行為學角度簡單分析這些行為的可能含義）
3. 💡 主人可以怎麼做（給飼主的建議）
4. 😂 一句話翻譯（用一句超短的話總結寵物想說的）

語調要可愛、幽默、有趣。繁體中文回答。內心獨白要有戲劇性。"""

            with st.spinner("🐾 正在與毛孩溝通中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是可愛的寵物翻譯師，用繁體中文翻譯動物的心聲，語調幽默溫馨。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.9,
                    max_tokens=1024,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader(f"🐾 {name_str}的心聲")
            st.markdown(result)

        except Exception as e:
            st.error(f"發生錯誤：{e}")

# --- 頁尾 ---
st.markdown("---")
st.caption("🐾 AI 寵物翻譯機 — 純屬娛樂，真正了解毛孩請諮詢獸醫")
