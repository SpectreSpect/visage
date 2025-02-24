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


def create_task(create_url, api_key):
    headers = {
        "Authorization": api_key
    }

    data = {
        "sourceImage": image_to_base64("data\images\kirill.jpg"),
        "faceImage": image_to_base64("data\images\maxim.jpg"),
        "webhook": None
    }
    
    response = requests.post(create_url, data=data, headers=headers)

    return response.json()["id"]


def get_task_result(result_url, api_key, task_id):
    headers = {
        "Authorization": api_key
    }

    response = requests.get(result_url + "?taskId=" + task_id, headers=headers)

    return response.json()


if __name__ == "__main__":
    load_dotenv()

    create_url = "https://gptunnel.ru/v1/faceswap/create"
    result_url = "https://gptunnel.ru/v1/faceswap/result"
    api_key = os.getenv("GPTUNNEL_API_KEY")
    
    # taks_id = create_task(create_url, api_key)
    # print(taks_id)
    result = get_task_result(result_url, api_key, "67bc8a97a161d00001440bf7")

    print(result["status"])

    print(result["result"])

    # print(response.json())