from src.api_clients.gptunnel_faceswap_api import GptunnelFaceSwapApi
from dotenv import load_dotenv
import os
from PIL import Image
import numpy as np


load_dotenv()
api_client = GptunnelFaceSwapApi(os.getenv("GPTUNNEL_API_KEY"))

# image1 = np.array(Image.open(r"D:\Projects\visage\data\images\sasha.jpg"))
# image2 = np.array(Image.open(r"D:\Projects\visage\data\images\Kirill.jpg"))

# json_response = api_client.create(image1, image2) # 67c1c59429a4290001e3e586

json_response = api_client.result("67c1c59429a4290001e3e586")

print(json_response)