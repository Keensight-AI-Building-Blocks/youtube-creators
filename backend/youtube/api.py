from backend.youtube.connect import service
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.youtube.connect import vector_store
import time


def get_comments(video_id, max_results=50):

    request = service.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        order="relevance",
        maxResults=max_results,
    )

    response = request.execute()
    comments = []
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    return comments


def get_trending_videos(category_id, max_results=10):

    request = service.videos().list(
        part="snippet,statistics,topicDetails",
        chart="mostPopular",
        regionCode="US",
        videoCategoryId=category_id,
        maxResults=max_results,
    )

    response = request.execute()

    trending_videos = []
    for item in response["items"]:
        video_info = {
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "description": item["snippet"]["description"],
            "published_at": item["snippet"]["publishedAt"],
            "view_count": item["statistics"]["viewCount"],
            "comment_count": item["statistics"].get("commentCount", "N/A"),
            "topic_categories": item["topicDetails"]["topicCategories"],
        }
        trending_videos.append(video_info)

    return trending_videos


def load_transcript(video_id):

    attempts = 0
    while attempts < 10:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            combined_text = " ".join([entry["text"] for entry in transcript])
            documents = [Document(page_content=combined_text)]
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            all_splits = text_splitter.split_documents(documents)
            vector_store.add_documents(documents=all_splits)
            return {
                "message": "Transcript loaded successfully.",
                "points_added": len(all_splits),
            }
        except Exception as e:
            attempts += 1
            if attempts == 10:
                return {
                    "message": "Failed to load transcript after 10 attempts.",
                    "error": str(e),
                }
            time.sleep(1)
