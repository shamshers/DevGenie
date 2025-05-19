from llm.claude_api import ClaudeClient

def review_code(code, rag_chain=None):
    claude = ClaudeClient()
    prompt = (
        f"Review the following Python code. "
        "Identify any issues, bugs, or improvements, and provide a fixed version if needed.\n\n"
        f"Code:\n{code}\n\n"
        "Reply with:\nIssues: <list of issues or 'None'>\nFixed Code: <only if issues found, else reply 'No change needed'>"
    )
    review = claude.generate(prompt)
    # Naive parsing
    if "Issues:" in review and "Fixed Code:" in review:
        issues = review.split("Issues:")[1].split("Fixed Code:")[0].strip()
        fixed_code = review.split("Fixed Code:")[1].strip()
    else:
        issues = review
        fixed_code = ""
    return issues, fixed_code
