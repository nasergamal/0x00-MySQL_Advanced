#!/usr/bin/env python3
'''python mongodb'''
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    '''insert document into school collection'''
    new = mongo_collection.insert_one(kwargs)
    return new.inserted_id
