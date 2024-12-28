from googleapiclient.discovery import build
from backend.config import config



def get_comments(video_id):
    api_key = config.get("YOUTUBE_API_KEY")
    service = build('youtube', 'v3', developerKey=api_key)

    request = service.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=50,
        order="relevance",
    )

    response = request.execute()
    print(response)
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments