# YouTube Creators

A FastAPI agentic service for Youtube creators.

## Features

- **Health Check Endpoint**: Check the health status of the service.
- **Metadata Endpoint**: Retrieve metadata about the service.
- **Trending Data Endpoints**: Fetch trending YouTube data.
- **Video Ideas Endpoint**: Generate video ideas based on trending data.

## Endpoints

### Health Check

- **GET** `/health`
  - Returns the health status of the service.

### Metadata

- **GET** `/metadata`
  - Returns metadata about the service.

### Trending Data

- **GET** `/trending`
  - Fetches a list of trending YouTube data.
  - Query Parameters:
    - `limit` (int): Number of records to fetch.
    - `offset` (int): Number of records to skip.

- **GET** `/trending/{video_id}`
  - Fetches detailed trending data for a specific video ID.
  - Path Parameters:
    - `video_id` (str): The ID of the video.

### Video Ideas

- **POST** `/video_ideas`
  - Generates video ideas based on trending data.
  - Request Body:
    - `category_id` (int): The category ID to filter trending data.
    - `date` (str): The end date for fetching trending data.
    - `buffer` (int): The number of days before the end date to start fetching data.

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

## Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```properties
DATABASE_URL = "postgresql://username:password@hostname:port/database_name"
DEBUG = 1
FRONTEND_ORIGINS = "http://localhost:3000"
API_KEY = "your_api_key_here"
MODEL_NAME = "gpt-4o-mini"
BASE_URL = "https://api.openai.com/v1/"
```

- `DATABASE_URL`: The URL for the PostgreSQL database.
- `DEBUG`: Set to `1` to enable debug mode.
- `FRONTEND_ORIGINS`: Comma-separated list of allowed origins for CORS.
- `API_KEY`: API key for external services.
- `MODEL_NAME`: The name of the model to use.
- `BASE_URL`: The base URL for API requests.

## Schemas

### TrendingDataSchema

Represents the schema for trending YouTube data.

- `video_id` (str): The ID of the video.
- `title` (str): The title of the video.
- `publishedAt` (datetime): The publication date of the video.
- `channelTitle` (str): The title of the channel.
- `categoryId` (int): The category ID of the video.
- `trending_date` (datetime): The date the video started trending.
- `tags` (str): The tags associated with the video.
- `view_count` (int): The number of views.
- `likes` (int): The number of likes.
- `dislikes` (int): The number of dislikes.
- `description` (str): The description of the video.

### TrendingDataDetailedSchema

Represents the detailed schema for a specific trending YouTube video.

- `video_id` (str): The ID of the video.
- `title` (str): The title of the video.
- `publishedAt` (datetime): The publication date of the video.
- `channelId` (str): The ID of the channel.
- `channelTitle` (str): The title of the channel.
- `categoryId` (int): The category ID of the video.
- `trending_date` (datetime): The date the video started trending.
- `tags` (str): The tags associated with the video.
- `view_count` (int): The number of views.
- `likes` (int): The number of likes.
- `dislikes` (int): The number of dislikes.
- `comment_count` (int): The number of comments.
- `thumbnail_link` (str): The link to the thumbnail image.
- `comments_disabled` (bool): Whether comments are disabled.
- `ratings_disabled` (bool): Whether ratings are disabled.
- `description` (str): The description of the video.

### GenerateVideoIdeasInput

Represents the input schema for generating video ideas.

- `category_id` (int): The category ID to filter trending data.
- `date` (str): The end date for fetching trending data.
- `buffer` (int): The number of days before the end date to start fetching data.

### VideoIdea

Represents a single video idea.

- `video_idea` (str): The generated video idea.

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
- `API_Key_Set` (bool): Indicates if the API key is set.
- `Model_Name` (str): The name of the model being used.
- `Base_URL` (str): The base URL for API requests.