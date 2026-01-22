# conversational.py
from llm import ollama_call
# CONVERSATIONAL AGENT (ACK ONLY)


def conversational_agent(text: str) -> str:
    prompt = f"""
User said:
"{text}"

Reply politely in ONE short sentence.

Rules:
- No questions
- No curiosity
- No repeated answers
"""
    return ollama_call(prompt, temperature=0.2)