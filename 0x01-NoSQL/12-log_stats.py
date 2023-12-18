#!/usr/bin/env python3
'''return collection's data using pymongo'''
from pymongo import MongoClient

if __name__ == "__main__":
    logs = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    print(logs.count_documents({}), 'logs')
    print('Methods:')
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for m in method:
        count = logs.count_documents({"method": m})
        print(f'\tmethod {m}: {count}')
    print(logs.count_documents({"method": "GET", "path": "/status"}),
          'status check')
