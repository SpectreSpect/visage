from src.image_uploaders.image_uploader import ImageUploader
import requests
import logging


class ImgbbImageUploader(ImageUploader):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.upload_url = "https://api.imgbb.com/1/upload"


    def upload(self, file_path: str) -> str:
        try:
            with open(file_path, "rb") as file:
                response = requests.post(
                    self.upload_url,
                    params={"key": self.api_key},
                    files={"image": file}
                )
                return response.json()["data"]["url"]
            
        except FileNotFoundError:
            error_msg = f"File not found at {file_path}"
        except requests.exceptions.RequestException as e:
            error_msg = f"Error uploading image: {e}"
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
        else:
            return None
        
        if self.debug:
            raise RuntimeError(error_msg)
        else:
            logging.error(error_msg)
            return None