from pymongo import MongoClient

DB_URI = "mongodb://localhost:27017"
DB_NAME = "tune_seek"

client = MongoClient(DB_URI)
db = client[DB_NAME]

def connect_db():
    print(f"Connected to MongoDB : {DB_URI}")

def store_fingerprint(title, artist, hashes):
    db.songs.insert_one({
        "title": title,
        "artist": artist,
        "hashes": hashes
    })
 