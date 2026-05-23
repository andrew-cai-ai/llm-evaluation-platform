import os
from typing import Dict, Any

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
)
def call_openai(prompt: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=10,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    return {
        "text": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens if response.usage else None,
        "output_tokens": response.usage.completion_tokens if response.usage else None,
        "total_tokens": response.usage.total_tokens if response.usage else None,
    }