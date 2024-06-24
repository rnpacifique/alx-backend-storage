#!/usr/bin/env python3
"""A Python function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """A Python function that returns all students sorted by average score"""
    all_students = mongo_collection.aggregate(
        [
            {
                '$project': {
                    '_id': 1,
                    'name': 1,
                    'averageScore': {
                        '$avg': {
                            '$avg': '$topics.score',
                        },
                    },
                    'topics': 1,
                },
            },
            {
                '$sort': {'averageScore': -1},
            },
        ]
    )
    return all_students