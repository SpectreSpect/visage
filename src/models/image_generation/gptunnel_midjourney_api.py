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
import logging


class GptunnelMidjourneyApi(ImageGenModelApi):
    def __init__(self, api_key: str, imgbb_api_key: str = None):
        super().__init__()
        self.api_key = api_key
        self.image_uploader = ImgbbImageUploader(imgbb_api_key) if imgbb_api_key is not None else None
        
    
    def __image_to_base64(self, image_path) -> str:
        mime_type, _ = mimetypes.guess_type(image_path)

        with open(image_path, "rb") as img_file:
            return f"data:{mime_type};base64," + base64.b64encode(img_file.read()).decode('utf-8')
    
    def _make_request(self, url: str, data: dict) -> dict:
        """Helper function to handle API requests and error handling."""
        headers = {"Authorization": self.api_key}
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            json_response = response.json()
            
            if "id" not in json_response:
                raise KeyError("Task ID not found in the response")

            return json_response
        
        except requests.Timeout:
            error_msg = "Request timed out while contacting Midjourney API"
        except requests.RequestException as e:
            error_msg = f"Midjourney API request failed: {str(e)}"
        except ValueError:
            error_msg = "Invalid JSON response from Midjourney API"
        except KeyError as e:
            error_msg = f"Key not found in the response: {str(e)}"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
        
        if self.debug:
            raise RuntimeError(error_msg)
        else:
            logging.error(error_msg)
            return None

    def create_imagine_task(self, prompt: str) -> GptunnelMidjourneyImagineTask:
        url = "https://gptunnel.ru/v1/midjourney/imagine"
        json_response = self._make_request(url, {"prompt": prompt})
        return GptunnelMidjourneyImagineTask(json_response["id"], self.api_key) if json_response else None
        
        # headers = {
        #     "Authorization": self.api_key
        # }
        
        # data = {
        #     "prompt": prompt
        # }

        # try: 
        #     response = requests.post(url, headers=headers, data=data)
        #     response.raise_for_status()

        #     json_response = response.json()
        #     if "id" not in json_response:
        #         raise KeyError("Task ID not found in the response")
            
        #     return GptunnelMidjourneyImagineTask(json_response, self.api_key)
        
        # except requests.Timeout:
        #     error_msg = "Request timed out while contacting Midjourney API"
        #     raise RuntimeError("Midjourney API request timed out")
        # except requests.RequestException as e:
        #     error_msg = f"Midjourney API request failed: {str(e)}"
        # except ValueError:
        #     error_msg = "Invalid JSON response from Midjourney API"
        # except KeyError as e:
        #     error_msg = f"Key not found in the response: {str(e)}"
        # except Exception as e:
        #     error_msg = f"Unexpected error: {str(e)}"
        
        # if self.debug:
        #     raise RuntimeError(error_msg)
        # else:
        #     logging.error(error_msg)
        #     return None
    
    
    def create_upscale_task(self, task: GptunnelMidjourneyImagineTask, image_id: int = 1):
        url = "https://gptunnel.ru/v1/midjourney/upsample"
        json_response = self._make_request(url, {"taskId": task.index, "image": image_id})
        return GptunnelMidjourneyUpscaleTask(json_response["id"], self.api_key) if json_response else None

        # headers = {
        #     "Authorization": self.api_key
        # }

        # data = {
        #     "taskId": task.index,
        #     "image": image_id
        # }

        # try: 
        #     response = requests.post(url, json=data, headers=headers)
        #     response.raise_for_status()

        #     json_response = response.json()
        #     if "id" not in json_response:
        #         raise KeyError("Task ID not found in the response")
            
        #     return GptunnelMidjourneyImagineTask(json_response["id"], self.api_key)
        
        # except requests.Timeout:
        #     error_msg = "Request timed out while contacting Midjourney API"
        #     raise RuntimeError("Midjourney API request timed out")
        # except requests.RequestException as e:
        #     error_msg = f"Midjourney API request failed: {str(e)}"
        # except ValueError:
        #     error_msg = "Invalid JSON response from Midjourney API"
        # except KeyError as e:
        #     error_msg = f"Key not found in the response: {str(e)}"
        # except Exception as e:
        #     error_msg = f"Unexpected error: {str(e)}"
        
        # if self.debug:
        #     raise RuntimeError(error_msg)
        # else:
        #     logging.error(error_msg)
        #     return None

    def generate_image(self, prompt: str, source_image_path: str = None, save_dir: str = "output") -> str:
        if source_image_path is not None:
            assert self.image_uploader is not None, "Image uploader is not set"
            
            source_image_url = self.image_uploader.upload(source_image_path)
            
            if source_image_url is None:
                return None
            
            prompt = f"{prompt} --cref {source_image_url}"

        image_gen_task = self.create_imagine_task(prompt)

        while image_gen_task.get_status() != "done":
            if image_gen_task.get_status() == "failed":
                return None
        
        upscale_task = self.create_upscale_task(image_gen_task)

        while upscale_task.get_status() != "done":
            if upscale_task.get_status() == "failed":
                return None

        image_url = upscale_task.get_result()

        os.makedirs(save_dir, exist_ok=True)

        output_image_path = os.path.join(save_dir, upscale_task.index + ".jpg")
        ImageLoader.download_image(image_url, output_image_path)

        # output_image = np.array(Image.open(output_image_path))
        return output_image_path