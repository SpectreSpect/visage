from src.image_uploaders.image_uploader import ImageUploader
import requests


class ImgbbImageUploader(ImageUploader):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.upload_url = "https://api.imgbb.com/1/upload"

    def upload(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            response = requests.post(
                self.upload_url,
                params={"key": self.api_key},
                files={"image": file}
            )
        
        return response.json()["data"]["url"]