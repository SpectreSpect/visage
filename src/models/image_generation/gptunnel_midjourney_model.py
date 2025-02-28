from src.models.image_generation.image_gen_model import ImageGenModel
from src.api_clients.gptunnel_midjourney_api import GptunnelMidjourneyApi
from src.image_loader import ImageLoader
import numpy as np
import time


class GptunnelMidjourneyModel(ImageGenModel):
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.api_client = GptunnelMidjourneyApi(api_key)
        self.image_loader = ImageLoader()
        self.generate_image_timeout = 120 # in seconds
        self.status_check_delay = 1

    def generate_image(self, prompt: str, reference_image: np.ndarray = None) -> np.ndarray:
        print("WARNING: reference_image in GptunnelMidjourneyModel is not handled yet!!!!!!!")
        
        json_response = self.api_client.imagine(prompt)
        task_id: str = json_response["id"]

        t1 = time.time()
        while True:
            json_response = self.api_client.result(task_id)

            if json_response["status"] == "done":
                break

            if json_response["status"] == "failed":
                raise RuntimeError("Image generation task failed.")
            
            t2 = time.time()
            if (t2 - t1) > self.generate_image_timeout:
                raise TimeoutError(f"Image generation timed out. "
                                   f"Exceeded timeout threshold of {self.generate_image_timeout} seconds.")

            time.sleep(self.status_check_delay)
        
        return self.image_loader.load(json_response["result"])