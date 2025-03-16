import os
from fastapi import APIRouter, File, UploadFile, Form
from models.database import db, store_fingerprint
from audio_processing.audio_fingerprinting import extract_fingerprint
from audio_processing.matcher import match_fingerprint, create_hashes

router = APIRouter()
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@router.get("/health")
async def get_health():
    return {"message : song route is healthy."}

@router.post("/upload")
async def upload_song(file: UploadFile = File(...), title: str = Form("title"), artist: str = Form("artist")):
    audio_path = os.path.join(UPLOADS_DIR, file.filename)

    #save file in the folder
    with open(audio_path, "wb") as buffer:
        buffer.write(await file.read())

    # extract fingerprint
    fingerprint = extract_fingerprint(audio_path)
    hashes = create_hashes(fingerprint)
    
    # store in DB
    store_fingerprint(title, artist, hashes)

    return {"message": f"{title} song added"}

@router.post("/match")
async def match_audio(file: UploadFile = File(...)):
    audio_path = os.path.join(UPLOADS_DIR, file.filename)
    
    # Save file locally
    with open(audio_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract fingerprints from query audio (only first 30 seconds)
    fingerprint = extract_fingerprint(audio_path, duration=20)
    audio_hashes = create_hashes(fingerprint)
    
    matches = match_fingerprint(audio_hashes)
    return {"matching songs " : matches.__str__()}
