from llm.claude_api import ClaudeClient

def generate_code(prompt, rag_chain):
    # Get docs/context from RAG (can be blank for now if not configured)
    try:
        context = rag_chain.run(prompt)
    except Exception:
        context = ""
    claude = ClaudeClient()
    system_prompt = (
        "You are a senior Python developer. Generate clean, correct, well-commented Python code for the following task."
    )
    user_prompt = f"Context:\n{context}\n\nTask:\n{prompt}\n\nPython code only, no extra commentary."
    code = claude.generate(user_prompt, system=system_prompt)
    return code
