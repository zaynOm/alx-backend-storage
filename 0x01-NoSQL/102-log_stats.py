#!/usr/bin/env python3
"Log stats - new version"

from pymongo import MongoClient


def nginx_logs():
    "provides some stats about Nginx logs stored in MongoDB"
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = client.logs.nginx

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_count = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_count} status check")

    ips = nginx_collection.aggregate(
        [
            {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10},
        ]
    )

    print("IPs:")
    for doc in ips:
        print(f"\t{doc.get('_id')}: {doc.get('count')}")


if __name__ == "__main__":
    nginx_logs()
