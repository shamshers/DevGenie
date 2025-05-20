import os
import anthropic


class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = "claude-3-opus-20240229"

    def generate(self, prompt, system=None, max_tokens=1024):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        resp = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages,
            temperature=0.2,
        )
        return resp.content[0].text
