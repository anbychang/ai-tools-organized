import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 二手定價助手", page_icon="🏷️", layout="centered")

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("取得 API Key：[Groq Console](https://console.groq.com/)")

st.title("🏷️ AI 二手定價助手")
st.caption("估算二手物品合理售價，推薦最佳販售平台")

# --- 物品資訊 ---
st.subheader("📦 物品資訊")

item_name = st.text_input("🏷️ 物品名稱", placeholder="例如：iPhone 15 Pro 256GB 藍色")

col1, col2 = st.columns(2)
with col1:
    purchase_price = st.number_input("💰 購買價格（NT$）", min_value=0, value=0, step=100)
    usage_time = st.selectbox(
        "⏰ 使用時間",
        ["未滿 1 個月", "1-3 個月", "3-6 個月", "6-12 個月", "1-2 年", "2-3 年", "3-5 年", "5 年以上"],
    )
with col2:
    condition = st.selectbox(
        "📋 物品狀況",
        ["全新未拆封", "近全新（幾乎無使用痕跡）", "良好（輕微使用痕跡）", "普通（明顯使用痕跡）", "堪用（有瑕疵但功能正常）"],
    )
    has_box = st.selectbox("📦 配件狀況", ["完整盒裝配件", "有盒但缺配件", "無盒有配件", "僅主體"])

extra_info = st.text_area(
    "📝 補充說明（選填）",
    height=80,
    placeholder="例如：有貼保護貼、電池健康度 92%、有一條小刮痕在背面...",
)

if st.button("💲 估算二手價格", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not item_name.strip():
        st.error("請輸入物品名稱。")
    else:
        prompt = (
            f"你是台灣二手物品定價專家，熟悉各大二手平台的行情。\n\n"
            f"物品資訊：\n"
            f"- 名稱：{item_name}\n"
            f"- 購買價格：NT${purchase_price:,}\n"
            f"- 使用時間：{usage_time}\n"
            f"- 物品狀況：{condition}\n"
            f"- 配件狀況：{has_box}\n"
            f"- 補充說明：{extra_info if extra_info.strip() else '無'}\n\n"
            "請提供：\n"
            "1. **建議售價區間**：最低價 / 建議價 / 理想價，並說明定價邏輯\n"
            "2. **快速出售價**：如果想快速賣掉的建議價格\n"
            "3. **推薦販售平台**：推薦 2-3 個最適合賣這個物品的平台（如蝦皮、旋轉拍賣、FB社團、PTT、Carousell等），並說明原因\n"
            "4. **賣場標題建議**：提供 2-3 個吸引人的賣場標題\n"
            "5. **提高售價的技巧**：如何讓物品賣到更好的價格\n\n"
            "請用繁體中文回答。"
        )

        try:
            client = Groq(api_key=api_key)
            with st.spinner("AI 正在評估二手行情..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是台灣二手物品定價專家，熟悉各平台行情與交易技巧。請用繁體中文提供準確的估價建議。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=1536,
                )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("💲 二手定價分析")
            st.markdown(result)
            st.info("💡 實際成交價可能因市場供需而異，建議參考平台上同類商品的實際成交紀錄。")
        except Exception as e:
            st.error(f"發生錯誤：{e}")
