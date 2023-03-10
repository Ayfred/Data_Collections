from googleapiclient.discovery import build
from os.path import abspath, dirname
import json
import pandas as pd


def safe_delete(comment, key):
    """ Deletes a key from a dict only if this key is contained in the dict """
    if key in comment:
        del comment[key]


def gather_comments_on_video(keyword):
    # Connect to Youtube API using the credentials saved in a different file
    f = open(f"{dirname(abspath(__file__))}\youtube_credentials.json", 'r', encoding='utf-8')
    data = json.load(f)
    f.close()
    youtube = build('youtube', 'v3', developerKey = data['api_key'])

    # First request: List the videos with the keyword {keyword}
    request = youtube.search().list(
            part="snippet",
            maxResults=50,
            order="viewCount",
            q=keyword
        )
    response = request.execute()

    comments = []
    users = dict()

    videos_count = len(response['items'])
    i = 0
    for video in response['items']:
        i += 1
        print(f"Treating video {i}/{videos_count}")
        # Get the comments and replies associated to this video ID
        request_comments = youtube.commentThreads().list(
            part="snippet, replies",
            order="relevance",
            videoId=video['id']['videoId'], 
            )
        # First page of comments for the video "video" (id: video['id']['videoId'])
        response_comments = request_comments.execute()

        while True:
            # Gather all the comments from this video in one list (top comments AND replies)
            for youtube_comment in response_comments['items']:
                topCom = youtube_comment['snippet']['topLevelComment']['snippet']
                topCom['parentId'] = None
                comments.append(topCom)
                if 'replies' in youtube_comment:
                    for reply in youtube_comment['replies']['comments']:
                        com = reply['snippet']
                        comments.append(com)

            # For each comment, delete the following fields: textDisplay, authorDisplayName, canRate, viewerRating, updatedAt, authorProfileImageUrl, authorChannelUrl
            # And map authorChannelId.value into authorChannelId
            for comment in comments:
                safe_delete(comment, 'textDisplay')
                safe_delete(comment, 'authorDisplayName')
                safe_delete(comment, 'canRate')
                safe_delete(comment, 'viewerRating')
                safe_delete(comment, 'updatedAt')
                safe_delete(comment, 'authorProfileImageUrl')
                safe_delete(comment, 'authorChannelUrl')
                if 'authorChannelId' in comment:
                    if type(comment['authorChannelId']) == dict:
                        comment['authorChannelId'] = comment['authorChannelId']['value']
                else:
                    comment['authorChannelId'] = 'Unknown'

            # Look for the next comments page, request the new comments
            if 'nextPageToken' in response_comments:
                request_comments_next = youtube.commentThreads().list(
                    part="snippet, replies",
                    order="relevance",
                    videoId=video['id']['videoId'], 
                    pageToken= response_comments['nextPageToken'],
                )
                response_comments = request_comments_next.execute()
            else:
                #Get out of the loop if no new comment page is available
                break
    
    # Save the comments and users into files
    print("Saving into files...")

    pretty_json = json.dumps(comments, indent=4, ensure_ascii=False) 
    with open(f"{dirname(abspath(__file__))}\youtube-{keyword}.json", 'w', encoding='utf-8') as outfile:
        outfile.write(pretty_json)

    df = pd.DataFrame(comments, columns=comments[0].keys())
    output_file_path_2 = f"{dirname(abspath(__file__))}\youtube-{keyword}-comments.xlsx"
    df.to_excel(output_file_path_2, index=False)


gather_comments_on_video('chatGPT')
