import streamlit as st
from agents.agent_controller import handle_user_request

# For demo: fallback if no RAG (no Qdrant running)
class DummyRAGChain:
    def run(self, prompt): return ""

# Replace with actual get_rag_chain from rag.rag_chain if Qdrant ready
rag_chain = DummyRAGChain()

st.set_page_config(page_title="DevGenie: GenAI Python Assistant", layout="wide")
st.title("🤖 DevGenie – Your Python AI Assistant")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_area("Enter your Python prompt, code for review, or explanation:")

if st.button("Submit") and user_input.strip():
    with st.spinner("DevGenie is working..."):
        result = handle_user_request(user_input, rag_chain)
        st.session_state["history"].append(
            {"user": user_input, "result": result}
        )

for chat in st.session_state["history"][::-1]:
    st.markdown(f"**You:** {chat['user']}")
    result = chat['result']
    if result.get('code'):
        st.subheader("📝 Generated Code")
        st.code(result['code'], language="python")
    if result.get('issues') and result['issues'] not in ["None", "", None]:
        st.subheader("🔍 Code Review")
        st.warning(result['issues'])
    if result.get('fixed_code') and result['fixed_code'].lower() != "no change needed":
        st.subheader("🛠️ Fixed Code")
        st.code(result['fixed_code'], language="python")
    if result.get('explanation'):
        st.subheader("💡 Explanation")
        st.success(result['explanation'])
    st.divider()

