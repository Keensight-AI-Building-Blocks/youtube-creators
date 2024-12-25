from typing import List
from datetime import datetime
from pydantic import BaseModel

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.config import config

from backend.db.connect import get_db, SessionLocal
from backend.db.schemas import (
    TrendingDataDetailedSchema,
    TrendingDataSchema,
    GenerateVideoIdeasInput,
    HealthCheckResponse,
    MetadataResponse,
)

from backend.agents.schemas import VideoIdeas
from backend.db import utils as db_utils

from backend.agents.workflows import generate_ideas_chain

DEBUG = config.get("DEBUG", cast=bool, default=False)
FRONTEND_ORIGINS = config.get(
    "FRONTEND_ORIGINS", cast=lambda x: [s.strip() for s in x.split(",")], default=""
)


app = FastAPI()
start_time = datetime.now()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/video_ideas", response_model=VideoIdeas)
async def execute(inputs: GenerateVideoIdeasInput):
    return generate_ideas_chain(
        category_id=inputs.category_id, date=inputs.date, buffer=inputs.buffer
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    uptime = datetime.now() - start_time
    return {
        "status": "healthy",
        "uptime": str(uptime),
        "current_time": datetime.now().isoformat(),
    }


@app.get("/metadata", response_model=MetadataResponse)
async def metadata():
    return {
        "Debug": DEBUG,
        "Frontend_Origins": FRONTEND_ORIGINS,
        "API_Key_Set": bool(config.get("API_KEY")),
        "Model_Name": config.get("MODEL_NAME"),
        "Base_URL": config.get("BASE_URL"),
    }


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
