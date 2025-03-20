from pydantic import BaseModel

class Tune(BaseModel):
    name: str
    artist: str
    url: str
    image: str