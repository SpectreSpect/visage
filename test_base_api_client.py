from src.api_clients.base_api_client import BaseApiClient
from api_clients.gptunnel_midjourney_api import GptunnelApiClient
from dotenv import load_dotenv
import os


load_dotenv()
api_client = BaseApiClient("https://gptunnel.ru", os.getenv("GPTUNNEL_API_KEY"))

# json_response = api_client.request("/v1/midjourney/imagine", "POST", 
#                                    data={"prompt": "A full-body portrait"}, return_type="json")
# print(json_response["id"])

# 67c1b2fe79e02a0001f70e8a

json_response = api_client.request("/v1/midjourney/result", "GET", 
                                   params={"taskId": "67c1bdb129a4290001e3e468"}, return_type="json")
print(json_response)


# json_response = api_client.request("/v1/midjourney/upsample", "POST", 
#                                    data={"taskId": "67c1bc7279e02a0001f70f61", "image": 1}, return_type="json")
# print(json_response)

# https://gptunnel.ru/v1/midjourney/upsample