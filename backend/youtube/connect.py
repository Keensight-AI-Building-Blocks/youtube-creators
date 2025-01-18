from googleapiclient.discovery import build
from backend.config import config
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import Distance, VectorParams

api_key = config.get("YOUTUBE_API_KEY", default="abc123")

if not api_key:
    raise ValueError("YOUTUBE_API_KEY is not set in the environment variables")

service = build("youtube", "v3", developerKey=api_key)

client = QdrantClient(path="./qdrant_data")
collection_name = "youtube_transcripts"
embeddings = OpenAIEmbeddings()

if collection_name not in [col.name for col in client.get_collections().collections]:
    client.create_collection(
        collection_name="youtube_transcripts",
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embeddings,
)
