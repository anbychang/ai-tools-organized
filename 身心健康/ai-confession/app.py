import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 告白產生器", page_icon="💕")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_confession(traits, how_met, style, extra):
    """呼叫 Groq API 產生告白訊息"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位浪漫的告白文案專家。請根據以下資訊，撰寫一段告白訊息：

- 對方的特質：{traits}
- 認識方式：{how_met}
- 告白風格：{style}
- 補充說明：{extra if extra else '無'}

請提供：
1. 一段完整的告白訊息（適合傳訊息、寫卡片、或面對面說）
2. 一段簡短版（適合突然鼓起勇氣時說）
3. 告白時機與場合建議
4. 如果對方猶豫時的應對建議

要求：
- 真誠不油膩
- 符合所選風格
- 有個人特色，不要太制式
- 讓對方感受到你的用心

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1500,
    )
    return response.choices[0].message.content


# 主頁面
st.title("💕 AI 告白產生器")
st.markdown("喜歡一個人卻不知道怎麼說？讓 AI 幫你寫出心動告白！")

st.markdown("---")

how_met = st.selectbox("你們怎麼認識的？", [
    "同學/同校", "同事", "朋友介紹", "社群/交友軟體",
    "活動/社團", "偶然相遇", "青梅竹馬", "其他"
])

style = st.radio(
    "告白風格",
    ["浪漫深情", "幽默搞笑", "直球對決", "文藝詩意"],
    horizontal=True,
)

traits = st.text_area(
    "對方的特質（越具體越好）",
    placeholder="例如：笑起來有酒窩、很會照顧人、喜歡看書、常常幫助別人...",
    height=100,
)

extra = st.text_area(
    "你們之間的小故事（選填）",
    placeholder="例如：有一次下雨他借我傘、我們常一起加班...",
    height=80,
)

if st.button("💝 產生告白訊息", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not traits:
        st.warning("請描述對方的特質！")
    else:
        with st.spinner("AI 正在幫你撰寫告白..."):
            try:
                result = generate_confession(traits, how_met, style, extra)
                st.markdown("### 💝 告白訊息")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
