import streamlit as st
from groq import Groq
from data.ingredients import INGREDIENT_CATEGORIES

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI 食譜推薦", page_icon="🍳", layout="wide")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    diet = st.selectbox("飲食偏好", ["無限制", "素食", "低醣", "無麩質"])
    servings = st.slider("份量（人數）", min_value=1, max_value=8, value=2)
    st.divider()
    st.caption("模型：llama-3.3-70b-versatile（Groq）")

# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------
st.title("🍳 AI 食譜推薦")
st.markdown("告訴 AI 你有哪些食材，它會為你推薦 2–3 道食譜！")

# ---------------------------------------------------------------------------
# Ingredient selection
# ---------------------------------------------------------------------------
selected_ingredients: list[str] = []

st.subheader("📦 選擇你的食材")

# Category checkboxes
tabs = st.tabs(list(INGREDIENT_CATEGORIES.keys()))
for tab, (category, items) in zip(tabs, INGREDIENT_CATEGORIES.items()):
    with tab:
        cols = st.columns(4)
        for idx, item in enumerate(items):
            with cols[idx % 4]:
                if st.checkbox(item, key=f"cb_{category}_{item}"):
                    selected_ingredients.append(item)

# Free-text input for extra ingredients
extra = st.text_input("其他食材（逗號分隔）", placeholder="例如：起司, 鮮奶油, 檸檬")
if extra:
    selected_ingredients.extend([i.strip() for i in extra.split(",") if i.strip()])

# Show current selection
if selected_ingredients:
    st.info(f"已選擇 **{len(selected_ingredients)}** 項食材：{', '.join(selected_ingredients)}")

# ---------------------------------------------------------------------------
# Generate recipes
# ---------------------------------------------------------------------------
def build_prompt(ingredients: list[str], diet: str, servings: int) -> str:
    diet_note = "" if diet == "無限制" else f"飲食限制：{diet}。"
    return (
        "你是一位專業的中式與亞洲料理廚師。\n"
        f"使用者手邊有以下食材：{', '.join(ingredients)}。\n"
        f"{diet_note}\n"
        f"請為 {servings} 人份推薦 2–3 道食譜。\n\n"
        "每道食譜請依照以下格式回覆（使用繁體中文）：\n"
        "### 菜名\n"
        "- **難度**：簡單 / 中等 / 困難\n"
        "- **烹飪時間**：約 XX 分鐘\n"
        "- **所需食材**：列出食材與份量\n"
        "#### 步驟\n"
        "1. …\n2. …\n"
        "#### 💡 小提示\n"
        "- …\n\n"
        "請確保步驟清楚、具體，份量標示明確。"
    )


def get_recipes(prompt: str, api_key: str) -> str:
    client = Groq(api_key=api_key)
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "你是一位專業廚師，擅長根據現有食材推薦美味又實用的食譜。請用繁體中文回答。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=4096,
    )
    return chat.choices[0].message.content


# Button
if st.button("🔍 取得食譜建議", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在左側欄輸入 Groq API Key。")
    elif not selected_ingredients:
        st.warning("請至少選擇一項食材。")
    else:
        prompt = build_prompt(selected_ingredients, diet, servings)
        with st.spinner("AI 正在構思食譜，請稍候…"):
            try:
                result = get_recipes(prompt, api_key)
                st.divider()
                st.subheader("🍽️ 推薦食譜")

                # Split by "###" to create expandable sections
                sections = [s.strip() for s in result.split("###") if s.strip()]
                if sections:
                    for section in sections:
                        lines = section.split("\n", 1)
                        title = lines[0].strip()
                        body = lines[1].strip() if len(lines) > 1 else ""
                        with st.expander(f"🥘 {title}", expanded=True):
                            st.markdown(body)
                else:
                    # Fallback: render the whole response
                    st.markdown(result)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
