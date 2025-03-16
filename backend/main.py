from fastapi import FastAPI
from routes.songs import router as song_router
from models.database import db
import uvicorn

app = FastAPI(title="TuneSeek", description="Shazam-like music recognition API")

# Include API routes
app.include_router(song_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)