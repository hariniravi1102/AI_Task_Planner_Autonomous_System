# confirmation.py
def confirm_prompt(user_inputs: str) -> str:
    return f"""
You are a GIS and Remote Sensing PLANNER.

Based ONLY on the user inputs below:
- Summarize the task in ONE clear sentence
- Do NOT add assumptions
- No technical details

Output format (STRICT):

Final understanding:
<one sentence>

Is this correct?

User inputs:
{user_inputs}
"""

def refine_prompt(prev_summary: str, refinement: str) -> str:
    return f"""
You are a GIS and Remote Sensing PLANNER.

Update the task understanding using the refinement text.

Previous understanding:
{prev_summary}

User refinement:
{refinement}

Output format (STRICT):

Final understanding:
<one sentence>

Is this correct?
"""



