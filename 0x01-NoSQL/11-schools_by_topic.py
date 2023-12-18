#!/usr/bin/env python3
'''return collection's data using pymongo'''
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    '''return all documents in a collection'''
    return(mongo_collection.find({"topics": topic}))
