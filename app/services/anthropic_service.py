import os
from anthropic import Anthropic


def call_anthropic(prompt: str,
                   model: str = "claude-3-5-haiku-latest"):

    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    response = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text