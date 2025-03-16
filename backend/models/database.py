from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from utils.logger import log_function

DB_URI = "mongodb://localhost:27017"
DB_NAME = "tune_seek"

client = MongoClient(DB_URI)
db = client[DB_NAME]

def connect_db():
    print(f"Connected to MongoDB : {DB_URI}")

def setup_indexes():
    # Create an index on the hash field (most important)
    db.songs.create_index([("hash", 1)])
    
    # If you already have a compound index for uniqueness
    # db.songs.create_index([("hash", 1), ("title", 1)], unique=True)
    
    print("Indexes created successfully")

def store_fingerprint(title, artist, hashes):
    """Stores a song's fingerprint hashes in the database, creating a new record for each hash."""
    
    # Ensure each hash is stored as an individual document
    documents = [{"title": title, "artist": artist, "hash": h[0], "offset_time": h[1]} for h in hashes]
    
    try:
        # Insert all documents at once for efficiency
        db.songs.insert_many(documents)
    except DuplicateKeyError as e:
        print(f"Duplicate entry skipped: {e}")

connect_db()
setup_indexes()