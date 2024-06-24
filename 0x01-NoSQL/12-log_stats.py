#!/usr/bin/env python3
"""
Script to provide stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


def count_logs(mongo_collection):
    """
    Count logs in collection
    """
    total_logs = mongo_collection.count_documents({})
    print("{} logs".format(total_logs))


def count_methods(mongo_collection):
    """
    Count methods
    """
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print("method {}: {}".format(method, count))


def status_check(mongo_collection):
    """
    Count logs with method=GET and path=/status
    """
    count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(count))


def main():
    """
    Main function
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    count_logs(logs_collection)
    print("Methods:")
    count_methods(logs_collection)
    status_check(logs_collection)


if __name__ == "__main__":
    main()