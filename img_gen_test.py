import requests
import os
from dotenv import load_dotenv
import base64
import mimetypes


def image_to_base64(image_path):
    # Get the MIME type of the image
    mime_type, _ = mimetypes.guess_type(image_path)

    with open(image_path, "rb") as img_file:
        # Convert the image to base64 and prepend the MIME type
        return f"data:{mime_type};base64," + base64.b64encode(img_file.read()).decode('utf-8')


def create_task(create_url, api_key, prompt: str):
    url = "https://gptunnel.ru/v1/midjourney/imagine"
    headers = {
        "Authorization": api_key
    }

    data = {
        # "sourceImage": image_to_base64("data\images\kirill.jpg"),
        # "faceImage": image_to_base64("data\images\maxim.jpg"),
        "prompt": prompt
    }
    
    response = requests.post(url, data=data, headers=headers)

    return response.json()["id"]


def get_task_result(api_key, task_id: str):
    url = "https://gptunnel.ru/v1/midjourney/result"
    headers = {
        "Authorization": api_key
    }

    response = requests.get(url + "?taskId=" + task_id, headers=headers)

    return response.json()

def upsample(api_key, task_id: str, image_id: int = 1):
    url = "https://gptunnel.ru/v1/midjourney/upsample"
    headers = {
        "Authorization": api_key
    }

    data = {
        # "sourceImage": image_to_base64("data\images\kirill.jpg"),
        # "faceImage": image_to_base64("data\images\maxim.jpg"),
        "taskId": task_id,
        "image": 1
    }
    
    response = requests.post(url, json=data, headers=headers)

    return response.json()["id"]


if __name__ == "__main__":
    load_dotenv()

    create_url = "https://gptunnel.ru/v1/midjourney/imagine"
    api_key = os.getenv("GPTUNNEL_API_KEY")
    
    # task_id = create_task(create_url, api_key, "Galactic cat")
    # print(task_id)

    # task_id = upsample(api_key, "67bc8dd4a161d00001440d23")
    # print(task_id)

    #67bc9118a161d00001440d8c

    result = get_task_result(api_key, "67bc9118a161d00001440d8c")

    # result = get_task_result(api_key, "67bc8dd4a161d00001440d23")

    print(result["status"])

    print(result["result"])

    # print(response.json())