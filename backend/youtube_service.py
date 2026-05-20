import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

def search_channel(youtube, company_name):
    try:
        request = youtube.search().list(
            part="snippet",
            q=company_name,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        if response["items"]:
            return response["items"][0]["snippet"]["channelId"]
        return None
    except Exception as e:
        print(f"Error searching channel for {company_name}: {e}")
        return None

def get_channel_stats(youtube, channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics,contentDetails",
            id=channel_id
        )
        response = request.execute()
        if response["items"]:
            channel = response["items"][0]
            stats = channel["statistics"]
            snippet = channel["snippet"]
            return {
                "channel_id": channel_id,
                "channel_name": snippet.get("title", "N/A"),
                "description": snippet.get("description", "N/A")[:300],
                "country": snippet.get("country", "N/A"),
                "created_at": snippet.get("publishedAt", "N/A"),
                "subscriber_count": int(stats.get("subscriberCount", 0)),
                "total_views": int(stats.get("viewCount", 0)),
                "total_videos": int(stats.get("videoCount", 0)),
                "uploads_playlist": channel["contentDetails"]["relatedPlaylists"]["uploads"]
            }
        return None
    except Exception as e:
        print(f"Error getting channel stats: {e}")
        return None

def get_recent_videos(youtube, uploads_playlist_id, max_results=10):
    try:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=uploads_playlist_id,
            maxResults=max_results
        )
        response = request.execute()
        video_ids = []
        for item in response["items"]:
            video_ids.append(item["contentDetails"]["videoId"])
        return video_ids
    except Exception as e:
        print(f"Error getting recent videos: {e}")
        return []

def get_video_stats(youtube, video_ids):
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=",".join(video_ids)
        )
        response = request.execute()
        videos = []
        for video in response["items"]:
            stats = video["statistics"]
            snippet = video["snippet"]
            videos.append({
                "video_id": video["id"],
                "title": snippet.get("title", "N/A"),
                "published_at": snippet.get("publishedAt", "N/A"),
                "description": snippet.get("description", "N/A")[:200],
                "tags": snippet.get("tags", [])[:5],
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
            })
        videos.sort(key=lambda x: x["view_count"], reverse=True)
        return videos
    except Exception as e:
        print(f"Error getting video stats: {e}")
        return []

def calculate_upload_frequency(videos):
    if len(videos) < 2:
        return "Not enough data"
    try:
        from datetime import datetime
        dates = []
        for v in videos:
            date_str = v["published_at"][:10]
            dates.append(datetime.strptime(date_str, "%Y-%m-%d"))
        dates.sort(reverse=True)
        if len(dates) >= 2:
            total_days = (dates[0] - dates[-1]).days
            if total_days == 0:
                return "Multiple videos per day"
            avg_days = total_days / (len(dates) - 1)
            if avg_days <= 3:
                return f"Every {round(avg_days, 1)} days (Very Active)"
            elif avg_days <= 7:
                return f"Every {round(avg_days, 1)} days (Weekly)"
            elif avg_days <= 14:
                return f"Every {round(avg_days, 1)} days (Bi-weekly)"
            else:
                return f"Every {round(avg_days, 1)} days (Infrequent)"
    except:
        return "Unable to calculate"

def get_channel_data(company_name):
    try:
        youtube = get_youtube_client()

        # Search for channel
        channel_id = search_channel(youtube, company_name)
        if not channel_id:
            return {
                "company": company_name,
                "error": "Channel not found",
                "channel_stats": None,
                "videos": [],
                "upload_frequency": "N/A",
                "avg_views": 0,
                "avg_likes": 0,
                "avg_comments": 0,
                "top_video": None
            }

        # Get channel statistics
        channel_stats = get_channel_stats(youtube, channel_id)
        if not channel_stats:
            return {
                "company": company_name,
                "error": "Could not fetch channel stats",
                "channel_stats": None,
                "videos": [],
                "upload_frequency": "N/A",
                "avg_views": 0,
                "avg_likes": 0,
                "avg_comments": 0,
                "top_video": None
            }

        # Get recent videos
        video_ids = get_recent_videos(youtube, channel_stats["uploads_playlist"], max_results=10)
        videos = []
        if video_ids:
            videos = get_video_stats(youtube, video_ids)

        # Calculate averages
        avg_views = sum(v["view_count"] for v in videos) // len(videos) if videos else 0
        avg_likes = sum(v["like_count"] for v in videos) // len(videos) if videos else 0
        avg_comments = sum(v["comment_count"] for v in videos) // len(videos) if videos else 0
        upload_frequency = calculate_upload_frequency(videos)
        top_video = videos[0] if videos else None

        return {
            "company": company_name,
            "error": None,
            "channel_stats": channel_stats,
            "videos": videos,
            "upload_frequency": upload_frequency,
            "avg_views": avg_views,
            "avg_likes": avg_likes,
            "avg_comments": avg_comments,
            "top_video": top_video
        }

    except Exception as e:
        print(f"Error fetching data for {company_name}: {e}")
        return {
            "company": company_name,
            "error": str(e),
            "channel_stats": None,
            "videos": [],
            "upload_frequency": "N/A",
            "avg_views": 0,
            "avg_likes": 0,
            "avg_comments": 0,
            "top_video": None
        }