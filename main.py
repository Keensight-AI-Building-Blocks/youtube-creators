from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from backend.config import config

from backend.db.connect import get_db, SessionLocal
from backend.db.schemas import TrendingDataDetailedSchema, TrendingDataSchema
from backend.db import utils as db_utils

DEBUG = config.get("DEBUG", cast=bool, default=False)
FRONTEND_ORIGINS = config.get(
    "FRONTEND_ORIGINS", cast=lambda x: [s.strip() for s in x.split(",")], default=""
)


class InputModel(BaseModel):
    data: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/execute")
async def execute(input: InputModel):
    result = input.data.upper()
    return {"result": result}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/metadata")
async def metadata():
    return {"Debug": DEBUG}


@app.get("/trending", response_model=List[TrendingDataSchema])
async def get_trending_data(
    db_session: SessionLocal = Depends(get_db), limit: int = 10, offset: int = 0
):
    return db_utils.get_trending_data(db_session, offset=offset, limit=limit)


@app.get("/trending/{video_id}", response_model=TrendingDataDetailedSchema)
async def get_trending_data_by_id(
    video_id: str, db_session: SessionLocal = Depends(get_db)
):
    data = db_utils.get_trending_data_single(db_session, video_id=video_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return data
