import base64
import logging
import sys
from io import BytesIO

from fastapi import FastAPI, BackgroundTasks
from PIL import Image
from pydantic import BaseModel

from fastapi_photo.utils import clean_client, raw_client, resize_image, write_to_blob


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

logging.getLogger("azure").setLevel(logging.ERROR)

MAX_IMAGE_SIZE = 30e6


class Photo(BaseModel):
    photo_base64: bytes
    name: str


app = FastAPI(debug=True)


@app.post("/photo")
async def post_photo(photo: Photo, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        write_to_blob,
        raw_client,
        base64.decodebytes(photo.photo_base64),
        f"{photo.name}.jpg",
    )

    return {"message": "Photo received"}


@app.post("/processPhoto")
async def process_photo(photo: Photo, background_tasks: BackgroundTasks):
    image_bytes = base64.decodebytes(photo.photo_base64)
    image = Image.open(BytesIO(image_bytes))

    size = len(image_bytes)
    image = resize_image(image, size, MAX_IMAGE_SIZE)

    io = BytesIO()
    image.save(io, format="PNG")

    background_tasks.add_task(
        write_to_blob, clean_client, io.getvalue(), f"{photo.name}.jpg"
    )
    return {"message": "Photo processed"}
