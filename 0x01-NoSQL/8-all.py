#!/usr/bin/env python3
'''return collection's data using pymongo'''
from pymongo import MongoClient


def list_all(mongo_collection):
    '''return all documents in a collection'''
    return(mongo_collection.find())
