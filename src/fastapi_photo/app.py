import base64

from fastapi import FastAPI
from pydantic import BaseModel


class Photo(BaseModel):
    photo_base64: bytes
    name: str

app = FastAPI()


@app.post("/photo")
async def post_photo(photo: Photo):

    with open(f"/app/data/{photo.name}.jpg", "wb+") as fh:
        fh.write(base64.decodebytes(photo.photo_base64))

    return {"message": "Photo received"}