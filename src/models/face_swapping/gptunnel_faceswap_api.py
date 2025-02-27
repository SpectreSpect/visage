from src.models.face_swapping.face_swap_model_api import FaceSwapModelApi
import numpy as np
import base64
import mimetypes
import requests
from src.models.data.gptunnel_faceswap_task import GptunnelFaceswaptask
import os
from src.image_loader import ImageLoader
from PIL import Image


class GptunnelFaceswapApi(FaceSwapModelApi):
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
    
    def __image_to_base64(self, image_path) -> str:
        mime_type, _ = mimetypes.guess_type(image_path)

        with open(image_path, "rb") as img_file:
            return f"data:{mime_type};base64," + base64.b64encode(img_file.read()).decode('utf-8')

    def create_faceswap_task(self, img1_path: str, img2_path: str) -> GptunnelFaceswaptask:
        url = "https://gptunnel.ru/v1/faceswap/create"

        headers = {
        "Authorization": self.api_key
        }

        data = {
            "sourceImage": self.__image_to_base64(img1_path),
            "faceImage": self.__image_to_base64(img2_path),
            "webhook": None
        }
        
        response = requests.post(url, data=data, headers=headers)

        task = GptunnelFaceswaptask(response.json()["id"], self.api_key)
        return task

    def swap_faces(self, img1_path: str, img2_path: str, save_dir: str = "output") -> str:
        task = self.create_faceswap_task(img1_path, img2_path)

        while task.get_status() != "done":
            if task.get_status() == "failed":
                return None
        
        image_url = task.get_result()
        
        os.makedirs(save_dir, exist_ok=True)

        output_image_path = os.path.join(save_dir, task.index + ".jpg")
        ImageLoader.download_image(image_url, output_image_path)

        # output_image = np.array(Image.open(output_image_path))
        return output_image_path