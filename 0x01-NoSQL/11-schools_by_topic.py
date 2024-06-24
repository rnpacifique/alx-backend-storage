#!/usr/bin/env python3
"""A Python function that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """Returns the list of schools having a specific topic"""
    query = {'topics': topic}
    schools = mongo_collection.find(query)
    return list(schools)