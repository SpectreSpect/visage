from src.models.image_generation.image_gen_model_api import ImageGenModelApi
from src.models.data.gptunnel_midjourney_imagine_task import GptunnelMidjourneyImagineTask
from src.models.data.gptunnel_midjourney_upscale_task import GptunnelMidjourneyUpscaleTask
import requests
from src.image_loader import ImageLoader
from src.image_uploaders.imgbb_image_uploader import ImgbbImageUploader
import os
from PIL import Image
import numpy as np
import base64
import mimetypes


class GptunnelMidjourneyApi(ImageGenModelApi):
    def __init__(self, api_key: str, imgbb_api_key: str = None):
        super().__init__()
        self.api_key = api_key
        self.image_uploader = ImgbbImageUploader(imgbb_api_key) if imgbb_api_key is not None else None
        
    
    def __image_to_base64(self, image_path) -> str:
        mime_type, _ = mimetypes.guess_type(image_path)

        with open(image_path, "rb") as img_file:
            return f"data:{mime_type};base64," + base64.b64encode(img_file.read()).decode('utf-8')

    def create_imagine_task(self, prompt: str) -> GptunnelMidjourneyImagineTask:
        url = "https://gptunnel.ru/v1/midjourney/imagine"
        
        headers = {
            "Authorization": self.api_key
        }
        
        data = {
            "prompt": prompt
        }

        response = requests.post(url, headers=headers, data=data)

        task = GptunnelMidjourneyImagineTask(response.json()["id"], self.api_key)
        return task
    
    
    def create_upscale_task(self, task: GptunnelMidjourneyImagineTask, image_id: int = 1):
        url = "https://gptunnel.ru/v1/midjourney/upsample"
        headers = {
            "Authorization": self.api_key
        }

        data = {
            "taskId": task.index,
            "image": image_id
        }
        
        response = requests.post(url, json=data, headers=headers)

        task = GptunnelMidjourneyUpscaleTask(response.json()["id"], self.api_key)
        return task

    def generate_image(self, prompt: str, source_image_path: str = None) -> str:
        if source_image_path is not None:
            assert self.image_uploader is not None, "Image uploader is not set"
            source_image_url = self.image_uploader.upload(source_image_path)
            prompt += f" --cref {source_image_url}"

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

        # output_image = np.array(Image.open(output_image_path))
        return output_image_path