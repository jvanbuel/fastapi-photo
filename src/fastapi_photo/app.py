import base64
import logging
import sys
from io import BytesIO

from fastapi import FastAPI
from PIL import Image
from pydantic import BaseModel

from fastapi_photo.utils import clean_client, raw_client, resize_image

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

logging.getLogger("azure").setLevel(logging.ERROR)

MAX_IMAGE_SIZE = 30e3


class Photo(BaseModel):
    photo_base64: bytes
    name: str


app = FastAPI(debug=True)


@app.post("/photo")
async def post_photo(photo: Photo):
    await raw_client.get_blob_client(f"{photo.name}.jpg").upload_blob(
        base64.decodebytes(photo.photo_base64),
        overwrite=True,
    )

    return {"message": "Photo received"}


@app.post("/processPhoto")
async def process_photo(photo: Photo):
    image_bytes = base64.decodebytes(photo.photo_base64)
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    size = len(image_bytes)
    image = resize_image(image, size, MAX_IMAGE_SIZE)

    io = BytesIO()
    image.save(io, format="JPEG")
    await clean_client.get_blob_client(f"{photo.name}.jpg").upload_blob(
        io.getvalue(),
        overwrite=True,
    )
    return {"message": "Photo processed"}
