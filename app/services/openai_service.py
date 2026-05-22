import os
from openai import OpenAI


def call_openai(prompt: str, model: str = "gpt-4o-mini") -> str:

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content