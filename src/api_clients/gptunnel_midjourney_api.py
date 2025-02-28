from src.api_clients.base_api_client import BaseApiClient
from src.utils.dict_utils import validate_dict
import requests
import time
import logging
import os


class GptunnelMidjourneyApi(BaseApiClient):
    
    def __init__(self, api_key, retries=3, backoff=2):
        super().__init__("https://gptunnel.ru", api_key, retries, backoff)

    def imagine(self, prompt: str, reference_image_url: str = None) -> dict:
        if reference_image_url is not None:
            prompt += f" --cref {reference_image_url}"

        json_response = self.request("/v1/midjourney/imagine", "POST", 
                                   data={"prompt": prompt}, return_type="json")
        return json_response
    
    def upsample(self, task_id: str, image_id: int = 1) -> dict:
        json_response = self.request("/v1/midjourney/upsample", "POST", 
                                   data={"taskId": task_id, "image": image_id}, return_type="json")
        return json_response
    
    def result(self, task_id: str) -> dict:
        json_response = self.request("/v1/midjourney/result", "GET", 
                                        params={"taskId": task_id}, return_type="json")
        return json_response
