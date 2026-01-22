#planner.py
from llm import ollama_call
# PLANNER PROMPTS


def form_prompt(task: str) -> str:
    return f"""
The task is to {task}.

You are a GIS and Remote Sensing PLANNER.

Your job:
- Extract IMPORTANT specification requirements from the user
- Present ALL questions at once
- Frame them like a USER INPUT FORM

Rules:
- Do NOT explain concepts
- Do NOT mention tools, algorithms, files, or code
- Ask ALL questions in a single response
- Keep everything optional

Presentation rules (STRICT):
- Each question MUST start with "# "
- Each selectable option MUST start with "- "
- One option per line
- Allow multiple selections
- Always include an option that can be clarified via notes
- Plain text only

Generate the input questions now.
"""
