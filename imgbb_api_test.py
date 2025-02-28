from src.api_clients.imgbb_api import ImgbbApi
from dotenv import load_dotenv
from PIL import Image
import numpy as np
import os


load_dotenv()
api_client = ImgbbApi(os.getenv("IMGBB_API_KEY"))

image = np.array(Image.open(r"D:\Projects\visage\data\images\Kirill.jpg"))

url = api_client.upload(image)

print(url)
