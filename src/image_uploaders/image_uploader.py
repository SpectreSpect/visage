from abc import ABC
import requests
import os


class ImageUploader(ABC):
    def __init__(self):
        self.debug = os.getenv("DEBUG", "False").lower() == "true"

    def upload(self, file_path: str) -> str:
        pass