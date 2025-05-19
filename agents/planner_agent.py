def plan(user_prompt):
    """Simple planner: decide pipeline based on user input."""
    prompt = user_prompt.lower()
    tasks = []
    if "review" in prompt or "fix" in prompt or "bug" in prompt:
        tasks.append({"type": "review", "content": user_prompt})
    if "explain" in prompt or "what does" in prompt:
        tasks.append({"type": "explain", "content": user_prompt})
    if not tasks:
        tasks.append({"type": "code_generation", "content": user_prompt})
        tasks.append({"type": "review", "content": user_prompt})
        tasks.append({"type": "explain", "content": user_prompt})
    return tasks
