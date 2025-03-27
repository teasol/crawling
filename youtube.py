from googleapiclient.discovery import build 
import time 
import json
import os

def get_replies(app, parent_id):
    replies = []
    request = app.comments().list(
        part="snippet",
        parentId=parent_id,
        maxResults=100
    )
    response = request.execute()
    for item in response.get('items', []):
        snippet = item['snippet']
        replies.append({
            'type': 'reply',
            'comment_id': item['id'],
            'parent_id': parent_id,
            'author': snippet.get('authorDisplayName'),
            'author_channel_id': snippet.get('authorChannelId', {}).get('value'),
            'text': snippet.get('textDisplay'),
            'published_at': snippet.get('publishedAt'),
            'like_count': snippet.get('likeCount')
        })

    return replies 

def main(app, video_id):
    comments_data = []
    next_page_token = None 

    while True:
        request = app.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            snippet = item['snippet']['topLevelComment']['snippet']
            comment_id = item['snippet']['topLevelComment']['id']
            comments_data.append({
                'type': 'comment',
                'comment_id': comment_id,
                'author': snippet.get('authorDisplayName'),
                'author_channel_id': snippet.get('authorChannelId', {}).get('value'),
                'text': snippet.get('textDisplay'),
                'published_at': snippet.get('publishedAt'),
                'like_count': snippet.get('likeCount')
            })

            if item['snippet']['totalReplyCount'] > 0:
                replies = get_replies(comment_id)
                comments_data.extend(replies)

        
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
        time.sleep(1)
    
    return comments_data

if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    video_id = "YOUTUBE_VIDEO_ID"
    youtube_build = build("youtube", "v3", developerKey=api_key)

    video_request = youtube_build.videos().list(
        part="snippet",
        id=video_id
    )
    video_response = video_request.execute()
    video_title = video_response['items'][0]['snippet']['title']
    
    output = main(youtube_build, video_id)
    
    if not os.path.exists("./result"):
        os.makedirs("./result")
    file_path = "./result/{video_title}_comments.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
