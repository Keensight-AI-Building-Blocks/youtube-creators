import pathlib
from decouple import Config, RepositoryEnv
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
ENV_FILE = BASE_DIR / ".env"

def get_config():
    if ENV_FILE.exists():
        return Config(RepositoryEnv(ENV_FILE))
    with open(ENV_FILE, "w") as f:
        f.write("DEBUG=True\n")
        f.write("DATABASE_URL=sqlite:///db.sqlite3\n")
        f.write("FRONTEND_ORIGINS=['*']\n")
        f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        f.write("MODEL_NAME=gpt-4o-mini\n")
        f.write("BASE_URL=https://api.openai.com/v1/\n")
        f.write("YOUTUBE_API_KEY=your_youtube_api_key_here\n")
        return Config(RepositoryEnv(ENV_FILE))
    
    from decouple import config as _decouple_config
    return _decouple_config

config = get_config()

def write_to_env_file(key: str, value: str):
    env_file_path = ".env"
    if os.path.exists(env_file_path):
        with open(env_file_path, "r") as env_file:
            lines = env_file.readlines()
        with open(env_file_path, "w") as env_file:
            for line in lines:
                if not line.startswith(f"{key}="):
                    env_file.write(line)
    with open(env_file_path, "a") as env_file:
        env_file.write(f"{key}={value}\n")