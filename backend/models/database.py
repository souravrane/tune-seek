from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from utils.logger import log_function

DB_URI = "mongodb://localhost:27017"
DB_NAME = "tune_seek"

client = MongoClient(DB_URI)
db = client[DB_NAME]

def connect_db():
    print(f"Connected to MongoDB : {DB_URI}")
    return db

def setup_indexes():
    db.tunes.create_index([("tune_id", 1)], unique=True)
    
    db.hashes.create_index([("tune_id", 1), ("hash", 1)])
    db.hashes.create_index([("hash", 1)])
    
    print("Indexes created successfully")

def store_tune(name, artist, url=None, image=None):
    tune_id = str(ObjectId())
    
    tune_doc = {
        "tune_id": tune_id,
        "name": name,
        "artist": artist,
        "url": url,
        "image": image
    }
    
    result = db.tunes.insert_one(tune_doc)
    return tune_id
    
def store_fingerprint(name, artist, hashes, url=None, image=None):
    tune_id = store_tune(name, artist, url, image)
    
    hash_docs = [ {"tune_id": tune_id, "hash": h[0], "offset": h[1]} for h in hashes]
    
    try:
        if hash_docs:
            db.hashes.insert_many(hash_docs)
            print(f"Stored {len(hash_docs)}  hashes for tune : {name}")
        else:
            print(f"No hashes to store for the tune {name}")
    except DuplicateKeyError as e:
        print(f"Duplicate entry skipped: {e}")

def get_tune_by_id(tune_id):
    return db.tunes.find_one({"tune_id": tune_id})

def find_matching_hashes(query_hash):
    return db.hashes.find({"hash": query_hash}, {"tune_id": 1, "offset": 1})

# Initialize db
connect_db()
setup_indexes()