# YouTube Creators

[![CI](https://github.com/Keensight-AI-Building-Blocks/youtube-creators/actions/workflows/ci.yaml/badge.svg)](https://github.com/Keensight-AI-Building-Blocks/youtube-creators/actions/workflows/ci.yaml)
![Coverage](static/coverage.svg)

A FastAPI agentic service for YouTube creators.

## Features

- **Video Ideas Endpoint**: Generate video ideas based on trending data.
- **Comment Analysis Endpoint**: Analyze comments for a specific video.
- **Health Check Endpoint**: Check the health status of the service.
- **Metadata Endpoint**: Retrieve metadata about the service.
- **Comments Data Endpoint**: Fetch comment data for a specific video.
- **Trending Data Endpoints**: Fetch trending YouTube data.
- **Load Transcript Endpoint**: Load YouTube transcript data into Qdrant.
- **Query Transcript Endpoint**: Query data from Qdrant using LangGraph.

## Endpoints

### Video Ideas

- **POST** `/generate_video_ideas`
  - Generates video ideas based on trending data.
  - Request Body:
    - `category_id` (int): The category ID to filter trending data.
  - Response:
    - `video_ideas` (list[VideoIdea]): A list of generated video ideas.

### Comment Analysis

- **POST** `/analyze_comments`
  - Analyzes comments for a specific video.
  - Request Body:
    - `video_id` (str): The ID of the video.
  - Response:
    - `strengths` (List[str]): List of strengths found in the comments.
    - `weaknesses` (List[str]): List of weaknesses found in the comments.
    - `opportunities` (List[str]): List of opportunities found in the comments.
    - `suggestions` (List[str]): List of suggestions found in the comments.
    - `overall_sentiment` (str): Describe overall sentiment of the comments.

### Health Check

- **GET** `/health`
  - Returns the health status of the service.
  - Response:
    - `status` (str): The health status of the service.
    - `uptime` (str): The uptime of the service.
    - `current_time` (str): The current time.

### Metadata

- **GET** `/metadata`
  - Returns metadata about the service.
  - Response:
    - `Debug` (bool): Indicates if debug mode is enabled.
    - `Frontend_Origins` (List[str]): List of allowed origins for CORS.
    - `OPENAI_API_Key_Set` (bool): Indicates if the API key is set.
    - `Model_Name` (str): The name of the model being used.
    - `Base_URL` (str): The base URL for API requests.
    - `YOUTUBE_API_Key_Set` (bool): Indicates if the YouTube API key is set.

### Fetch Comments

- **POST** `/get_comments`
  - Fetches comments for a specific video.
  - Request Body:
    - `video_id` (str): The ID of the video.
  - Response:
    - `Comments` (List[str]): A list of comments.

### Fetch Trending Videos

- **POST** `/get_trending_videos`
  - Fetches trending videos for a specific category.
  - Request Body:
    - `category_id` (str): The category ID to filter trending data.
  - Response:
    - `Videos` (List[TrendingVideo]): A list of trending videos.

### Load Transcript

- **POST** `/load`
  - Loads YouTube transcript data into Qdrant.
  - Request Body:
    - `video_id` (str): The ID of the video.
  - Response:
    - `message` (str): Success message.
    - `points_added` (int): Number of points added to Qdrant.

### Query Transcript

- **POST** `/query`
  - Queries data from Qdrant using LangGraph.
  - Request Body:
    - `query` (str): The query string.
    - `chat_history` (list[str]): The chat history.
  - Response:
    - `answer` (str): The answer to the query.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Keensight-AI-Building-Blocks/youtube-creators/tree/main
   cd youtube-creators
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   poetry install
   poetry shell
   ```

3. Set up the environment variables:
   ```bash
   # Update the .env file with the necessary details
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## Setting Up Qdrant Using Docker

1. Pull the Qdrant Docker image:
   ```bash
   docker pull qdrant/qdrant
   ```

2. Run the Qdrant container:
   ```bash
   docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
   ```

3. Verify that Qdrant is running by accessing `http://localhost:6333` in your browser.

## Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```properties
DATABASE_URL = "postgresql://username:password@hostname:port/database_name"
DEBUG = 1
FRONTEND_ORIGINS = "http://localhost:3000"
OPENAI_API_KEY = "your_api_key_here"
MODEL_NAME = "gpt-4o-mini"
BASE_URL = "https://api.openai.com/v1/"
YOUTUBE_API_KEY = "youtube_api_key"
```

- `DATABASE_URL`: The URL for the PostgreSQL database.
- `DEBUG`: Set to `1` to enable debug mode.
- `FRONTEND_ORIGINS`: Comma-separated list of allowed origins for CORS.
- `OPENAI_API_KEY`: API key for OpenAI.
- `MODEL_NAME`: The name of the model to use.
- `BASE_URL`: The base URL for API requests.
- `YOUTUBE_API_KEY`: API key for YouTube.

## Schemas

### CommentAnalysis

Represents the schema for analyzing comments.

- `strengths` (List[str]): List of strengths found in the comments.
- `weaknesses` (List[str]): List of weaknesses found in the comments.
- `opportunities` (List[str]): List of opportunities found in the comments.
- `suggestions` (List[str]): List of suggestions found in the comments.
- `overall_sentiment` (str): Describe overall sentiment of the comments.

### VideoIdeas

Represents a list of video ideas.

- `video_ideas` (list[VideoIdea]): A list of generated video ideas.

### HealthCheckResponse

Represents the response schema for the health check endpoint.

- `status` (str): The health status of the service.
- `uptime` (str): The uptime of the service.
- `current_time` (str): The current time.

### MetadataResponse

Represents the response schema for the metadata endpoint.

- `Debug` (bool): Indicates if debug mode is enabled.
- `Frontend_Origins` (List[str]): List of allowed origins for CORS.
- `OPENAI_API_Key_Set` (bool): Indicates if the API key is set.
- `Model_Name` (str): The name of the model being used.
- `Base_URL` (str): The base URL for API requests.
- `YOUTUBE_API_Key_Set` (bool): Indicates if the YouTube API key is set.

### YoutubeComments

Represents the schema for YouTube comments.

- `Comments` (List[str]): A list of comments.

### TrendingVideo

Represents the schema for a trending video.

- `title` (str): The title of the video.
- `channel` (str): The channel that published the video.
- `description` (str): The description of the video.
- `published_at` (str): The publication date of the video.
- `view_count` (str): The view count of the video.
- `comment_count` (str): The comment count of the video.
- `topic_categories` (List[str]): The topic categories of the video.

### LoadDataRequest

Represents the request schema for loading YouTube transcript data.

- `video_id` (str): The ID of the video.

### LoadDataResponse

Represents the response schema for loading YouTube transcript data.

- `message` (str): Success message.
- `points_added` (int): Number of points added to Qdrant.

### QueryRequest

Represents the request schema for querying data from Qdrant.

- `query` (str): The query string.
- `chat_history` (list[str]): The chat history.

### QueryResponse

Represents the response schema for querying data from Qdrant.

- `answer` (str): The answer to the query.
