# app.py
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from schemas import ChatInput, Task, UserInputs, Refinement, AOIInput, ExternalInput
from llm import ollama_call

from agents.understand import understanding_agent
from agents.conversational import conversational_agent
from agents.steering import steering_agent
from agents.planner import form_prompt
from agents.confirmation import confirm_prompt, refine_prompt
from upload import upload_files, save_aoi, save_external

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(inp: ChatInput):
    intent = understanding_agent(inp.message)

    if intent == "CHAT":
        reply = conversational_agent(inp.message)
        steer = steering_agent()
        return {
            "type": "CHAT",
            "response": f"{reply} {steer}"
        }

    return {
        "type": "GIS_TASK",
        "message": "I understand this is a GIS or remote sensing task. Let’s collect the required inputs."
    }

@app.post("/generate-form")
def generate_form(inp: Task):
    return {"form": ollama_call(form_prompt(inp.task))}

@app.post("/confirm")
def confirm(inp: UserInputs):
    return {"confirmation": ollama_call(confirm_prompt(inp.text))}

@app.post("/refine")
def refine(inp: Refinement):
    return {
        "confirmation": ollama_call(
            refine_prompt(inp.previous_summary, inp.refinement_text)
        )
    }
# upload
@app.post("/upload")
def upload(
    job_id: str = Form(...),
    files: List[UploadFile] = File(...)
):
    return upload_files(job_id, files)

# save AOI
@app.post("/save-aoi")
def save_aoi_route(inp: AOIInput):
    return save_aoi(inp.job_id, inp.geojson)

# save external preference
@app.post("/save-external")
def save_external_route(inp: ExternalInput):
    return save_external(inp.job_id, inp.text)