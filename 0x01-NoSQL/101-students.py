#!/usr/bin/env python3
'''python mongod'''
from pymongo import MongoClient


def top_students(mongo_collection):
    '''return student in descending order'''
    return (mongo_collection.aggregate(
        [
            {"$unwind": "$topics"},
            {"$group": {
                    "_id": "$_id",
                    "name": {"$first": "$name"},
                    "averageScore": {"$avg": "$topics.score"},
            }},
            {"$sort": {"averageScore": -1}}
        ]))
