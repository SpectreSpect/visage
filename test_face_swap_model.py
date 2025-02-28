from src.models.face_swapping.gptunnel_faceswap_model import GptunnelFaceSwapModel
from dotenv import load_dotenv
from PIL import Image
import numpy as np
import os



load_dotenv()
model = GptunnelFaceSwapModel(os.getenv("GPTUNNEL_API_KEY"))

image1 = np.array(Image.open(r"D:\Projects\visage\data\images\sasha.jpg"))
image2 = np.array(Image.open(r"D:\Projects\visage\data\images\Kirill.jpg"))

image = model.swap_faces(image2, image1)

Image.fromarray(image).save("tmp/test_output_image.png")
