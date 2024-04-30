#!/usr/bin/env python3
"Log stats"

if __name__ == "__main__":
    from itertools import zip_longest
    from pymongo import MongoClient

    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = client.logs.nginx

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    res = nginx_collection.aggregate(
        [
            {"$match": {"method": {"$in": methods}}},
            {"$group": {"_id": "$method", "count": {"$count": {}}}},
        ]
    )

    for method, doc in zip_longest(methods, res):
        if doc:
            print(f"\tmethod {method}: {doc.get('count')}")
        else:
            print(f"\tmethod {method}: 0")

    status_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_count} status check")
