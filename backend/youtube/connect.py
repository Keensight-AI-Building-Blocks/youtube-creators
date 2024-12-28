from googleapiclient.discovery import build
from backend.config import config


api_key = config.get("YOUTUBE_API_KEY")

service = build('youtube', 'v3', developerKey=api_key)
