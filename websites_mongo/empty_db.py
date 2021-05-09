from pymongo import MongoClient
import pymongo


def empty_DB():
	cluster = MongoClient('mongodb://localhost:27017/vrem_reduceri_db')
	db = cluster['vrem_reduceri_db']

	for coll in db.list_collection_names():
		collection = db[f'{coll}']
		collection.delete_many({})


if __name__ == '__main__':
	empty_DB()
