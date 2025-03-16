from pydantic import BaseModel
from typing import List

class Song(BaseModel):
    title: str
    artist: str
    hash : tuple
    offset_time: int