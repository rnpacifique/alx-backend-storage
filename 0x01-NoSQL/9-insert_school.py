#!/usr/bin/env python3
"""A Python function that inserts a new document in a collection based
on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on keyword argument"""
    new_document = kwargs
    insert_result = mongo_collection.insert_one(new_document)
    return insert_result.inserted_id