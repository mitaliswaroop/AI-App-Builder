# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Import your compiled agent from graph.py
from agent import graph

app = FastAPI()

# Allow React to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate_app(req: PromptRequest):
    # 1. Run the LangGraph agent
    result = graph.invoke(
        {"user_prompt": req.prompt},
        {"recursion_limit": 100}
    )

    # 2. Read the generated files from the output directory
    project_dir = "generated_project"
    files = {}

    if os.path.exists(project_dir):
        for filename in os.listdir(project_dir):
            filepath = os.path.join(project_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    files[filename] = f.read()

    # 3. Return the files to React
    return {"status": "success", "files": files}

# Run with: uvicorn api:app --reload