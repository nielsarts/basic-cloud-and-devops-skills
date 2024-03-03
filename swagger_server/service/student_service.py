import os
import tempfile
from functools import reduce
from bson import json_util
import json
from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient

# get the mongo uri from the environment
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(MONGO_URI)
db = client["swagger_server_db"]
col = db["students"]   

def add(student=None):
    res = col.find({"student_id": int(student.student_id), "first_name": student.first_name, "last_name": student.last_name})
    if len(list(res)) > 0:
        return 'already exists', 409

    x = col.insert_one(student.to_dict())
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = col.find_one({"student_id": student_id},{"_id": 0})
    if not student:
        return 'not found', 404
    
    return json.loads(json_util.dumps(student))

def delete(student_id=None):
    student = col.find_one({"student_id": int(student_id)})
    if not student:
        return 'not found', 404
    col.delete_one({"student_id": int(student_id)})
    return student_id