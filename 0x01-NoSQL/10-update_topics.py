#!/usr/bin/env python3
'''python mongodb'''
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    '''update documents in a collection'''
    mongo_collection.update_many({'name': name}, {"$set": {"topics": topics}})
