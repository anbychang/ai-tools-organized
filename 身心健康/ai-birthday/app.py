import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 生日祝福", page_icon="🎂")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("使用 Llama 3.3 70B 模型")


def generate_birthday(relationship, traits, style, extra):
    """呼叫 Groq API 產生生日祝福"""
    client = Groq(api_key=api_key)

    prompt = f"""你是一位才華洋溢的祝福文案專家。請根據以下資訊，撰寫個人化的生日祝福訊息：

- 與壽星的關係：{relationship}
- 壽星的特質/興趣：{traits}
- 祝福風格：{style}
- 補充說明：{extra if extra else '無'}

請提供：
1. 一段完整的生日祝福訊息（適合傳訊息或寫卡片）
2. 一段簡短版（適合群組或社群留言）
3. 一段搞笑/創意版（可選擇使用）

要求：
- 不要太制式、太罐頭
- 融入對方的特質，讓人感受到用心
- 根據關係調整親密程度
- 溫暖有溫度

請用繁體中文回答，格式清晰美觀。"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=1500,
    )
    return response.choices[0].message.content


# 主頁面
st.title("🎂 AI 生日祝福產生器")
st.markdown("告別罐頭祝福！讓 AI 幫你寫出最有溫度的生日訊息！")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    relationship = st.selectbox("與壽星的關係", [
        "好朋友", "普通朋友", "家人/親戚", "同事",
        "男友/女友/伴侶", "老師/前輩", "客戶/合作夥伴"
    ])
with col2:
    style = st.selectbox("祝福風格", [
        "溫馨感人", "搞笑幽默", "文青詩意", "正式得體", "甜蜜浪漫"
    ])

traits = st.text_area(
    "壽星的特質或興趣",
    placeholder="例如：愛旅行、最近在學吉他、是個超級貓奴、工作很拼命...",
    height=100,
)

extra = st.text_area(
    "你們之間的回憶或想說的話（選填）",
    placeholder="例如：謝謝他去年陪我度過低潮期...",
    height=80,
)

if st.button("🎉 產生生日祝福", type="primary", use_container_width=True):
    if not api_key:
        st.error("請在側邊欄輸入 Groq API Key！")
    elif not traits:
        st.warning("請輸入壽星的特質或興趣！")
    else:
        with st.spinner("AI 正在為壽星寫祝福..."):
            try:
                result = generate_birthday(relationship, traits, style, extra)
                st.markdown("### 🎉 生日祝福")
                st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
