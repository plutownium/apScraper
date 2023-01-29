from dotenv import load_dotenv
import os
from pymongo import MongoClient

from canadaAps.scraper.Logger import report_progress

load_dotenv()

mongo_pw = os.getenv("MONGO_PW")


conn_str = f"mongodb+srv://plutownium:{mongo_pw}@cluster0.eruuecx.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)


def get_mongo_client():
    return client


print("Connecting to mongodb: ")

client = get_mongo_client()
db = client["cel_logs"]
collection = db["scans"]


def write_log(task_id, provider, lat, long, num_of_results):
    log = make_log(task_id, provider, lat, long, num_of_results)
    print(report_progress("Logged to MongoDB: " + str(log)))
    collection.insert_one(log)


def make_log(task_id, provider, lat, long, num_of_results):
    return {"task_id": task_id, "provider": provider, "lat": lat, "long": long, "num_of_results": num_of_results}


def get_scan_collection():
    mongo_client = get_mongo_client()
    logs_db = mongo_client["cel_logs"]
    scan_coll = logs_db["scans"]
    return scan_coll


def get_all_logs(target_collection):
    return target_collection.find()


def convert_doc_to_dict(doc):
    return {
        "task_id": doc["task_id"],
        "provider": doc["provider"],
        "lat": doc["lat"],
        "long": doc["long"]
    }

