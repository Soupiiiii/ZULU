"""
ZULU Chat — LLM-powered conversation via OpenAI API
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are ZULU, an advanced AI assistant inspired by J.A.R.V.I.S from Iron Man.
You are intelligent, articulate, slightly formal, and occasionally witty.
Keep responses concise (2-3 sentences) unless the user asks for detail.
You are loyal to your user and always refer to them as 'sir' or 'ma'am'."""


def ask_llm(prompt: str, history: list = None) -> str:
    """Send a prompt to the LLM and return the response."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"I'm experiencing a technical issue: {e}"
