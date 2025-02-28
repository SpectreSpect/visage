from src.models.image_generation.image_gen_model import ImageGenModel
from src.api_clients.gptunnel_midjourney_api import GptunnelMidjourneyApi
from src.api_clients.imgbb_api import ImgbbApi
from src.image_loader import ImageLoader
import numpy as np
import time


class GptunnelMidjourneyModel(ImageGenModel):
    
    def __init__(self, api_key: str, imgbb_api_key: str):
        super().__init__()
        self.api_key = api_key
        self.imgbb_api_key = imgbb_api_key
        self.api_client = GptunnelMidjourneyApi(api_key)
        self.imgbb_api_client = ImgbbApi(imgbb_api_key)
        self.image_loader = ImageLoader()
        self.generate_image_timeout = 120 # in seconds
        self.status_check_delay = 1

    def generate_image(self, prompt: str, reference_image: np.ndarray = None) -> np.ndarray:
        if reference_image is not None:
            reference_image_url = self.imgbb_api_client.upload(reference_image)
            prompt += f" --cref {reference_image_url}"
        
        json_response = self.api_client.imagine(prompt)
        generation_task_id: str = json_response["id"]

        self.api_client.wait_for_task_completion(generation_task_id, self.generate_image_timeout)
        
        json_response = self.api_client.upsample(generation_task_id)
        upsampling_task_id: str = json_response["id"]

        json_response = self.api_client.wait_for_task_completion(upsampling_task_id, self.generate_image_timeout)

        # t1 = time.time()
        # while True:
        #     json_response = self.api_client.result(task_id)

        #     if json_response["status"] == "done":
        #         break

        #     if json_response["status"] == "failed":
        #         raise RuntimeError("Image generation task failed.")
            
        #     t2 = time.time()
        #     if (t2 - t1) > self.generate_image_timeout:
        #         raise TimeoutError(f"Image generation timed out. "
        #                            f"Exceeded timeout threshold of {self.generate_image_timeout} seconds.")

        #     time.sleep(self.status_check_delay)
        
        # json_response = self.api_client.upsample(task_id)

        
        return self.image_loader.load(json_response["result"])