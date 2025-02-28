from src.api_clients.base_api_client import BaseApiClient
from src.utils.image_utils import image_to_base64
import requests
import time
import logging
import os
import numpy as np


class GptunnelFaceSwapApi(BaseApiClient):
    
    def __init__(self, api_key, retries=3, backoff=2):
        super().__init__("https://gptunnel.ru", api_key, retries, backoff)
        self.session.headers.update({"Authorization": self.api_key})
    
    def create(self, source_image: np.ndarray, face_image: np.ndarray) -> dict:
        data = {
            "sourceImage": image_to_base64(source_image),
            "faceImage": image_to_base64(face_image),
            "webhook": None
        }

        json_response = self.request("v1/faceswap/create", "POST", data=data, return_type="json")
        return json_response
    
    def result(self, task_id: str) -> dict:
        json_response = self.request("v1/faceswap/result", "GET", 
                                        params={"taskId": task_id}, return_type="json")
        return json_response