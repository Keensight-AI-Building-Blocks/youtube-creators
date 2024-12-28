from backend.youtube.connect import service


def get_comments(video_id,max_results=50):

    request = service.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        order="relevance",
        maxResults=max_results
    )

    response = request.execute()
    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
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
    for item in response['items']:
        video_info = {
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'description': item['snippet']['description'],
            'published_at': item['snippet']['publishedAt'],
            'view_count': item['statistics']['viewCount'],
            'comment_count': item['statistics'].get('commentCount', 'N/A'),
            'topic_categories': item['topicDetails']['topicCategories']
        }
        trending_videos.append(video_info)

    return trending_videos