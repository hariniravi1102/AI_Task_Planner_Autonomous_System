#steering.py
from llm import ollama_call
# STEERING AGENT (NON-PREDEFINED)

def steering_agent() -> str:
    prompt = """
tell how much interested to do GIS and Remote sensing task

Rules:-
- No questions
- No repetition
- Neutral and friendly
"""
    return ollama_call(prompt, temperature=0.4)