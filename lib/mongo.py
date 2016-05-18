#!/usr/bin/python

import pymongo
from collections import defaultdict
import json

URI = "mongodb://writer:writer123@ds019482.mlab.com:19482/analytics"

_client = None
def _mongoclient():
	global _client, URI
	if _client is None:
		_client = pymongo.MongoClient(URI)
	return _client


_database = None
def _database_analytics():
	global _database
	if _database is None:
		_database = _mongoclient()['analytics']
	return _database

_collection_1 = None
def _collection_youtube_movie_trailers():
	global _collection_1
	if _collection_1 is None:
		_collection_1 = _database_analytics()['youtube_movie_trailers']
	return _collection_1

_collection_2 = None
def _collection_youtube_statistics():
	global _collection_2
	if _collection_2 is None:
		_collection_2 = _database_analytics()['youtube_statistics']
	return _collection_2

_data_1 = None
def data_youtube_movie_trailers():
	global _data_1
	if _data_1 is None:
		_data_1 = _collection_youtube_movie_trailers().find_one()
		if _data_1 is not None:
			_data_1.pop('_id')
	return _data_1

_data_2 = None
def data_youtube_statistics():
	global _data_2
	if _data_2 is None:
		_data_2 = _collection_youtube_statistics().find_one()
		if _data_2 is not None:
			_data_2.pop('_id')
	return _data_2

def write_youtube_statistics(data):
	try:
		_collection_youtube_statistics().insert_one(data)
	except Exception:
		return False
	return True

def get_graph_data():
	mov = _collection_youtube_movie_trailers().find_one()
	names = dict()
	for k in mov.keys():
		if k == '_id':
			continue	
		names[k] = mov[k]['name']

	view_counts = list()
	c = 1
	for rec in _collection_youtube_statistics().find():
		rr = dict()
		for k in rec.keys():
			if k == '_id':
				continue
			name = names[k]
			rr['timestamp'] = rec[k]['timestamp']
			rr[name] = rec[k]['viewCount']
		view_counts.append(rr)
	ret = dict()
	ret['data'] = view_counts
	ret['xkey'] = 'timestamp'
	ret['ykeys'] = names.values()
	ret['labels'] = names.values()
	return json.dumps(ret)