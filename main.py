from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.config import config, write_to_env_file

from backend.db.schemas import (
    HealthCheckResponse,
    MetadataResponse,
    SetEnvVarInput,
    SetEnvVarsInput,
)


from backend.agents.schemas import (
    CommentAnalysis,
    QueryRequest,
    QueryResponse,
)

from backend.youtube.api import get_comments, get_trending_videos, load_transcript
from backend.youtube.schemas import (
    YoutubeComments,
    TrendingVideos,
    LoadDataRequest,
    LoadDataResponse,
)


from backend.agents.workflows import (
    generate_video_ideas,
    analyze_comments,
    query_transcripts,
    rag_graph,
)


DEBUG = config.get("DEBUG", cast=bool, default=False)
FRONTEND_ORIGINS = config.get(
    "FRONTEND_ORIGINS", cast=lambda x: [s.strip() for s in x.split(",")], default="*"
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


@app.post("/load", response_model=LoadDataResponse)
async def load_data(request: LoadDataRequest):
    return load_transcript(request.video_id)


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    return query_transcripts(request.query, [])


@app.post("/query_test")
async def query_test(request: QueryRequest):
    res = rag_graph.invoke({"question": request.query, "context": request.chat_history})
    return {"answer": res["answer"], "retrieval_context": res["context"]}


@app.post("/analyze_comments", response_model=CommentAnalysis)
async def execute_analyze_comments(request: Request):
    data = await request.json()
    video_id = data.get("video_id")
    return analyze_comments(video_id)


@app.post("/generate_video_ideas")
async def execute_generate_video_ideas(request: Request):
    data = await request.json()
    category_id = data.get("category_id")
    return generate_video_ideas(category_id)


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
        "OPENAI_API_Key_Set": bool(config.get("OPENAI_API_KEY", default="")),
        "Model_Name": config.get("MODEL_NAME", default=""),
        "Base_URL": config.get("BASE_URL", default=""),
        "YOUTUBE_API_Key_Set": bool(config.get("YOUTUBE_API_KEY", default="")),
    }


@app.post("/get_comments", response_model=YoutubeComments)
async def fetch_comments(request: Request):
    data = await request.json()
    video_id = data.get("video_id")
    return {"Comments": get_comments(video_id)}


@app.post("/get_trending_videos", response_model=TrendingVideos)
async def fetch_trending_videos(request: Request):
    data = await request.json()
    category_id = data.get("category_id")
    return {"Videos": get_trending_videos(category_id)}


@app.post("/set_env_vars")
async def set_env_vars(input: SetEnvVarsInput):
    for key, value in input.vars.items():
        write_to_env_file(key, value)
    return {"status": "success"}
