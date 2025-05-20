import re

def plan(user_prompt):
    prompt = user_prompt.lower()
    tasks = []

    # If user pastes code and asks nothing else, assume review+explain
    if re.match(r'^\s*def\b|\s*class\b', prompt) or 'import ' in prompt:
        tasks.append({"type": "review", "content": user_prompt})
        tasks.append({"type": "explain", "content": user_prompt})
        return tasks

    # Generate code
    if re.search(r"\b(write|generate|create|function|script|class|python code|program)\b", prompt):
        tasks.append({"type": "code_generation", "content": user_prompt})
    # Review code
    if re.search(r"\b(review|fix|find bug|error|issue|correct|improve)\b", prompt):
        tasks.append({"type": "review", "content": user_prompt})
    # Explain code
    if re.search(r"\b(explain|describe|how does|what does|meaning)\b", prompt):
        tasks.append({"type": "explain", "content": user_prompt})

    # If no clear intent, default to code gen, review, explain
    if not tasks:
        tasks = [
            {"type": "code_generation", "content": user_prompt},
            {"type": "review", "content": user_prompt},
            {"type": "explain", "content": user_prompt},
        ]
    return tasks
