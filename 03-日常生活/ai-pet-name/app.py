import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 寵物取名", page_icon="🐾")
st.title("🐾 AI 寵物取名大師")
st.subheader("為你的毛孩取一個獨特又可愛的名字")

# 側邊欄設定
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.divider()
    st.markdown("### 使用說明")
    st.markdown("1. 輸入 Groq API Key\n2. 選擇動物種類\n3. 描述寵物特徵\n4. 點擊取名")

# 主要內容
animal = st.selectbox("🐶 選擇動物種類", ["貓", "狗", "兔", "鳥", "倉鼠", "烏龜"])

col1, col2 = st.columns(2)
with col1:
    breed = st.text_input("🏷️ 品種", placeholder="例如：布偶貓、柴犬、垂耳兔...")
    color = st.text_input("🎨 毛色/外觀", placeholder="例如：橘白相間、全黑、灰色...")
with col2:
    personality = st.text_input("💫 個性特徵", placeholder="例如：活潑、黏人、傲嬌、安靜...")
    gender = st.selectbox("⚤ 性別", ["不確定", "公", "母"])

name_style = st.multiselect(
    "🎯 命名風格偏好（可多選）",
    ["可愛", "搞笑", "文青", "日系", "英文", "食物相關", "古風"],
    default=["可愛"]
)

if st.button("✨ 幫我取名", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key！")
    elif not breed and not personality and not color:
        st.warning("請至少填寫一項寵物特徵！")
    else:
        prompt = f"""你是一位創意寵物命名專家。請根據以下寵物資訊，產生 10 個可愛又有意義的名字。

動物種類：{animal}
品種：{breed if breed else '未知'}
毛色/外觀：{color if color else '未知'}
個性特徵：{personality if personality else '未知'}
性別：{gender}
命名風格偏好：{'、'.join(name_style)}

請用繁體中文回答，為每個名字提供：
1. **名字**（如果是中文名也附上適合的英文暱稱）
2. **含義/命名理由** - 為什麼這個名字適合這隻{animal}
3. **暱稱** - 日常可以怎麼叫

請排版整齊，每個名字用分隔線隔開，讓主人容易選擇。"""

        try:
            client = Groq(api_key=api_key)
            with st.spinner("正在發揮創意取名中..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.9,
                    max_tokens=3000,
                )
            st.markdown("---")
            st.markdown(f"### 🎉 為你的{animal}推薦的名字")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"發生錯誤：{e}")
