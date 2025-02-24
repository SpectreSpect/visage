from abc import ABC
import requests


class ImageUploader(ABC):
    def __init__(self):
        pass

    def upload(self, file_path: str) -> str:
        pass