# llm.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"

# FASTAPI APP


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# OLLAMA CALL


def ollama_call(prompt: str, temperature: float = 0.3) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": 350
            }
        },
        timeout=(10, 180)
    )
    r.raise_for_status()
    return r.json()["response"].strip()