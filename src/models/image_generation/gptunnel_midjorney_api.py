from src.models.image_generation.image_gen_model_api import ImageGenModelApi
from src.models.data.gptunnel_midjourney_imagine_task import GptunnelMidjorneyImagineTask
from src.models.data.gptunnel_midjourney_upscale_task import GptunnelMidjorneyUpscaleTask
import requests
from src.image_loader import ImageLoader
import os
from PIL import Image
import numpy as np


class GptunnelMidjorneyApi(ImageGenModelApi):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def create_imagine_task(self, prompt: str) -> GptunnelMidjorneyImagineTask:
        url = "https://gptunnel.ru/v1/midjourney/imagine"
        
        headers = {
            "Authorization": self.api_key
        }
        
        data = {
            "prompt": prompt
        }

        response = requests.post(url, headers=headers, data=data)

        task = GptunnelMidjorneyImagineTask(response.json()["id"], self.api_key)
        return task
    
    
    def create_upscale_task(self, task: GptunnelMidjorneyImagineTask, image_id: int = 1):
        url = "https://gptunnel.ru/v1/midjourney/upsample"
        headers = {
            "Authorization": self.api_key
        }

        data = {
            "taskId": task.index,
            "image": image_id
        }
        
        response = requests.post(url, json=data, headers=headers)

        task = GptunnelMidjorneyUpscaleTask(response.json()["id"], self.api_key)
        return task

    def generate_image(self, prompt: str) -> np.ndarray:
        image_gen_task = self.create_imagine_task(prompt)

        while image_gen_task.get_status() != "done":
            if image_gen_task.get_status() == "failed":
                return None
        
        upscale_task = self.create_upscale_task(image_gen_task)

        while upscale_task.get_status() != "done":
            if upscale_task.get_status() == "failed":
                return None

        image_url = upscale_task.get_result()

        os.makedirs(self.output_dir, exist_ok=True)

        output_image_path = os.path.join(self.output_dir, upscale_task.index + ".jpg")
        ImageLoader.download_image(image_url, output_image_path)

        output_image = np.array(Image.open(output_image_path))
        return output_image