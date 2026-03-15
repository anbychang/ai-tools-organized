import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI 合約審查助手", page_icon="📜")

st.title("📜 AI 合約審查助手")
st.markdown("貼上合約文字，AI 幫你找出不公平條款、風險與缺漏。")

# --- 免責聲明 ---
st.warning(
    "⚠️ **免責聲明**：本工具僅提供初步參考意見，不構成法律建議。"
    "合約相關決策請務必諮詢專業律師。AI 分析可能有疏漏，"
    "請勿僅依賴本工具做出法律判斷。"
)

# --- 側邊欄 ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Groq API Key", type="password", placeholder="輸入你的 Groq API Key")
    st.markdown("---")
    st.markdown("### 審查重點")
    st.markdown(
        "- 不公平條款\n"
        "- 隱藏風險\n"
        "- 缺少的保護措施\n"
        "- 模糊不清的用語\n"
        "- 違約責任"
    )

# --- 主要輸入 ---
contract_type = st.selectbox(
    "📋 合約類型",
    ["租賃合約", "勞動合約/聘僱合約", "買賣合約", "服務合約", "合作合約",
     "保密合約 (NDA)", "加盟合約", "借貸合約", "其他"],
)

my_role = st.selectbox(
    "👤 你在合約中的角色",
    ["甲方（出租方/雇主/賣方）", "乙方（承租方/受僱方/買方）", "不確定"],
)

contract_text = st.text_area(
    "📄 貼上合約內容",
    placeholder="將合約全文或部分條款貼在這裡...",
    height=300,
)

focus = st.text_input(
    "🔍 特別關注的部分（選填）",
    placeholder="例如：違約金條款、競業禁止條款...",
)

# --- 審查合約 ---
if st.button("🔍 開始審查", type="primary", use_container_width=True):
    if not api_key:
        st.error("請先在側邊欄輸入 Groq API Key。")
    elif not contract_text:
        st.error("請貼上合約內容。")
    elif len(contract_text) < 50:
        st.error("合約內容太短，請貼上更完整的條款。")
    else:
        prompt = (
            f"你是一位經驗豐富的法律顧問。請審查以下合約，從保護我方權益的角度進行分析。\n\n"
            f"合約類型：{contract_type}\n"
            f"我的角色：{my_role}\n"
            f"特別關注：{focus if focus else '全面審查'}\n\n"
            f"合約內容：\n{contract_text}\n\n"
            f"請用繁體中文回答，分析以下面向：\n"
            f"1. **不公平條款**：哪些條款明顯偏向對方？\n"
            f"2. **風險提醒**：哪些條款可能造成我方損失？\n"
            f"3. **模糊用語**：哪些用詞不夠明確，可能造成爭議？\n"
            f"4. **缺少的保護**：合約中缺少哪些應有的保護條款？\n"
            f"5. **修改建議**：針對問題條款提出具體修改方向\n"
            f"6. **整體評估**：用 1-10 分評估合約對我方的友好程度\n\n"
            f"請在最後提醒使用者：此分析僅供參考，正式簽約前應諮詢專業律師。"
        )

        client = Groq(api_key=api_key)

        with st.spinner("AI 正在審查合約..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "你是專業的法律顧問，擅長合約審查與風險分析。請用繁體中文回答。"},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.5,
                    max_tokens=4096,
                )
                result = response.choices[0].message.content
                st.markdown("---")
                st.subheader("📋 審查報告")
                st.markdown(result)
                st.info("💡 提醒：以上分析僅供參考，正式簽約前請務必諮詢專業律師。")
            except Exception as e:
                st.error(f"發生錯誤：{e}")
