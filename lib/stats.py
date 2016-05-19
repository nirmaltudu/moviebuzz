import time
from apiclient.discovery import build  
import mongo
from datetime import datetime
from collections import defaultdict

DEVELOPER_KEY = "AIzaSyCW9a_Dq3EtJFisysq5rtiQ3iFI_2OZkPU"  
YOUTUBE_API_SERVICE_NAME = "youtube"  
YOUTUBE_API_VERSION = "v3"

_yt_client = None
def _youtube_client():
	global _yt_client, YOUTUBE_API_VERSION, YOUTUBE_API_SERVICE_NAME, DEVELOPER_KEY
	if _yt_client is None:
		_yt_client = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    					developerKey=DEVELOPER_KEY)
	return _yt_client


def stats():
	key_data = mongo.data_youtube_movie_trailers()
	data = dict()
	for vid in key_data.keys():
		data[vid] = get_stat(vid)
	return data

def write_stats():
	data = stats()
	return mongo.write_youtube_statistics(data)

def get_stat(vid):
	stats_list = _youtube_client().videos().list(id=vid,
                                part='id,statistics').execute()
	try:
	    stat = stats_list['items'][0]['statistics']
	    stat['timestamp'] = str(datetime.now())
	except KeyError:
		return {}
	return stat

def get_comment_threads():
	mov = mongo._collection_youtube_movie_trailers().find_one()
	names = dict()
	for k in mov.keys():
		if k == '_id':
			continue	
		names[k] = mov[k]['name']

	allComments = defaultdict(str)
	tempComments = list()
	for video in names.keys():
		time.sleep(1.0)
  		results = _youtube_client().commentThreads().list(
    		part="snippet",
    		videoId=video,
    		textFormat="plainText",
    		maxResults=20,
    		order='relevance'
  		).execute()

  		
  		for item in results["items"]:
  			comment = item["snippet"]["topLevelComment"]
  			tempComment = dict(videoId=video, videoName=names[video],
  								nbrReplies = item["snippet"]["totalReplyCount"],
  								author = comment["snippet"]["authorDisplayName"],
  								likes = comment["snippet"]["likeCount"],
  								publishedAt=comment["snippet"]["publishedAt"],
  								text = comment["snippet"]["textDisplay"].encode('utf-8').strip())
  			allComments[video] += tempComment['text'].lower().decode('utf-8').strip(":,.!?")
  			tempComments.append(tempComment)
  	
  	return allComments