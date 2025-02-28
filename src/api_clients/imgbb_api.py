from src.api_clients.base_api_client import BaseApiClient
from src.utils.image_utils import image_to_base64
import requests
from PIL import Image
from io import BytesIO
import numpy as np


class ImgbbApi(BaseApiClient):
    
    def __init__(self, api_key, retries=3, backoff=2):
        super().__init__("https://api.imgbb.com", api_key, retries, backoff)
    
    def upload(self, image: np.ndarray, buffer_image_format="PNG") -> str:
        pil_image = Image.fromarray(image)

        buffer = BytesIO()
        pil_image.save(buffer, format=buffer_image_format)
        buffer.seek(0)

        file_extension = buffer_image_format.lower()

        buffer_image_name = f"image.{file_extension}"
        buffer_image_type = f"image/{buffer_image_format.lower()}"
        json_response = self.request("/1/upload", "POST", 
                                params={"key": self.api_key},
                                files={"image": (buffer_image_name, buffer, buffer_image_type)})

        return json_response["data"]["url"]