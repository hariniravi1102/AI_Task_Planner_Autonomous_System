# schemas.py
from pydantic import BaseModel

class ChatInput(BaseModel):
    message: str

class Task(BaseModel):
    task: str

class UserInputs(BaseModel):
    text: str

class Refinement(BaseModel):
    previous_summary: str
    refinement_text: str

class AOIInput(BaseModel):
    job_id: str
    geojson: dict

class ExternalInput(BaseModel):
    job_id: str
    text: str
