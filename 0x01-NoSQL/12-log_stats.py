#!/usr/bin/env python3
"Log stats"

from itertools import zip_longest
from pymongo import MongoClient


def nginx_logs():
    "provides some stats about Nginx logs stored in MongoDB"
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = client.logs.nginx

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    res = nginx_collection.aggregate(
        [
            {"$match": {"method": {"$in": methods}}},
            {"$group": {"_id": "$method", "count": {"$count": {}}}},
            {"$sort": {"count": -1}},
        ]
    )

    for method, doc in zip_longest(methods, res):
        count = doc.get("count") if doc else 0
        print(f"\tmethod {method}: {count}")

    status_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_count} status check")


if __name__ == "__main__":
    nginx_logs()
