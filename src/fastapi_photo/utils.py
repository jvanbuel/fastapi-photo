import math

from azure.identity import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient
from PIL import Image

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

STORAGE_ACCOUNT = "fastapiphoto"


def resize_image(image: Image, size: int, max_size: int) -> Image:
    if size < max_size:
        logger.info("Image is small enough, not resizing")
        return image

    logger.info("Resizing image...")
    ratio = max_size / size
    (x, y) = image.size
    image.thumbnail((x * math.sqrt(ratio), y * math.sqrt(ratio)))
    return image


raw_client, clean_client = (
    BlobServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/",
        credential=DefaultAzureCredential(),
    ).get_container_client(container)
    for container in ("raw", "clean")
)


async def write_to_blob(client: BlobServiceClient, data: bytes, name: str) -> None:
    logger.info(f"Writing {name} to blob")
    await client.get_blob_client(name).upload_blob(
        data,
        overwrite=True,
    )
    logger.info(f"Finished writing {name} to blob")
