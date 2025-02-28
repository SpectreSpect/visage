from api_clients.gptunnel_midjourney_api import GptunnelApiClient
from dotenv import load_dotenv
import os


load_dotenv()
api_client = GptunnelApiClient(os.getenv("GPTUNNEL_API_KEY"))

# json_response = api_client.imagine("A full-body portrait", "https://s0.rbk.ru/v6_top_pics/media/img/8/21/756702418915218.jpg")
# print(json_response["id"])

json_response = api_client.result("67c1bc7279e02a0001f70f61")

# 67c1b2fe79e02a0001f70e8a

# json_response = api_client.upsample("67c1b2fe79e02a0001f70e8a", 3)

# json_response = api_client.request("/v1/midjourney/result", "GET", 
#                                    params={"taskId": "67c1b2fe79e02a0001f70e8a"}, return_type="json")
print(json_response)