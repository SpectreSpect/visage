from src.models.face_swapping.face_swap_model import FaceSwapModel
from src.api_clients.gptunnel_faceswap_api import GptunnelFaceSwapApi
from src.image_loader import ImageLoader
import numpy as np
import time


class GptunnelFaceSwapModel(FaceSwapModel):
    
    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key
        self.api_client = GptunnelFaceSwapApi(api_key)
        self.image_loader = ImageLoader()
        self.generate_image_timeout = 120 # in seconds
        self.status_check_delay = 1
    
    def swap_faces(self, source_image: np.ndarray, face_image: np.ndarray) -> np.ndarray:
        json_response = self.api_client.create(source_image, face_image)
        task_id: str = json_response["id"]

        t1 = time.time()
        while True:
            json_response = self.api_client.result(task_id)

            if json_response["status"] == "done":
                break

            if json_response["status"] == "failed":
                raise RuntimeError("Face swapping task failed.")
            
            t2 = time.time()
            if (t2 - t1) > self.generate_image_timeout:
                raise TimeoutError(f"Face swapping timed out. "
                                   f"Exceeded timeout threshold of {self.generate_image_timeout} seconds.")

            time.sleep(self.status_check_delay)
        
        return self.image_loader.load(json_response["result"])
