import base64
from uuid import uuid4

from locust import HttpUser, between, task


class PhotoProcessUser(HttpUser):
    wait_time = between(1, 5)
    userId = None

    @task
    def post_photo(self):
        with open("test.jpg", "rb") as fh:
            photo_base64 = base64.encodebytes(fh.read()).decode("utf-8")
            self.client.post(
                "/processPhoto",
                json={"name": str(self.userId), "photo_base64": photo_base64},
            )

    def on_start(self):
        self.userId = uuid4()


class PhotoUploadUser(HttpUser):
    wait_time = between(1, 5)
    userId = None

    @task
    def post_photo(self):
        with open("test.jpg", "rb") as fh:
            photo_base64 = base64.encodebytes(fh.read()).decode("utf-8")
            self.client.post(
                "/photo",
                json={"name": str(self.userId), "photo_base64": photo_base64},
            )

    def on_start(self):
        self.userId = uuid4()
