from apiclient.discovery import build  
import mongo
from datetime import datetime

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