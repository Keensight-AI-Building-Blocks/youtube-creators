from fastapi import FastAPI
from pydantic import BaseModel


class InputModel(BaseModel):
    data: str


app = FastAPI()


@app.post("/execute")
async def execute(input: InputModel):
    result = input.data.upper()
    return {"result": result}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/metadata")
async def metadata():
    return {"version": "1.0.0"}
