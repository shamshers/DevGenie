import os
import string

import anthropic

class ClaudeClient:
    def __init__(self, model="claude-3-opus-20240229"):
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            raise ValueError("CLAUDE_API_KEY environment variable not set.")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model


    def generate(self, prompt, system=string, max_tokens=1024, temperature=0.2):

        """
        Calls Anthropic Claude to generate a response.

        :param prompt: User's prompt (string)
        :param system: System prompt for Claude's behavior (string, optional)
        :param max_tokens: Max tokens in response
        :param temperature: Generation temperature
        :return: The response string
        """
        # Ensure system is a string if provided
        if system is not None and not isinstance(system, str):
            system = str(system)

        messages = [{"role": "user", "content": prompt}]
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages,
            system=system,  # system prompt goes here (must be a string or None)
            temperature=temperature,
        )
        # Claude v3 returns response.content as a list of message blocks
        return response.content[0].text if response.content else ""
