from langchain_openai import ChatOpenAI
from backend.config import config


MODEL_NAME = config.get("MODEL_NAME", cast=str, default="gpt-4o-mini")
API_KEY = config.get("API_KEY", cast=str, default="")
BASE_URL = config.get("BASE_URL", cast=str, default="https://api.openai.com/v1/")

model = ChatOpenAI(model=MODEL_NAME, api_key=API_KEY, base_url=BASE_URL)