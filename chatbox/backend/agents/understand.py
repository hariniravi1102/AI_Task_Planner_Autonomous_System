#understand.py
from llm import ollama_call

# UNDERSTANDING AGENT


def understanding_agent(text: str) -> str:
    prompt = f"""
Is this message about a GIS or remote sensing task?

Message:
"{text}"

Answer ONLY:
GIS_TASK or CHAT
"""
    out = ollama_call(prompt, temperature=0.0).upper()
    return "GIS_TASK" if "GIS_TASK" in out else "CHAT"