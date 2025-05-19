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
    st.markdown("**DevGenie Response:**")
    if "code" in chat['result']:
        st.code(chat['result']['code'], language="python")
    if "issues" in chat['result'] and chat['result']['issues']:
        st.warning(f"Issues Found: {chat['result']['issues']}")
    if "fixed_code" in chat['result'] and chat['result']['fixed_code']:
        st.code(chat['result']['fixed_code'], language="python")
    if "explanation" in chat['result']:
        st.success(f"Explanation: {chat['result']['explanation']}")
    st.divider()
