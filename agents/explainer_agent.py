from llm.claude_api import ClaudeClient

def explain_code(code, rag_chain=None):
    claude = ClaudeClient()
    prompt = (
        "Explain the following Python code in simple, clear language for a beginner. "
        "Mention what the code does and important concepts used.\n\n"
        f"Code:\n{code}\n"
    )
    explanation = claude.generate(prompt)
    return explanation
