import os
import anthropic

class ClaudeClient:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = "claude-3-opus-20240229"

    def generate(self, prompt, system=None, max_tokens=1024):
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            system=system,
            temperature=0.2,
        )
        # Claude v3 returns list of MessageBlocks; get the text block.
        return resp.content[0].text
