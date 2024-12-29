from googleapiclient.discovery import build
from backend.config import config


api_key = config.get("YOUTUBE_API_KEY", default="abc123")

service = build('youtube', 'v3', developerKey=api_key)
