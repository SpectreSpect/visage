from src.models.image_generation.gptunnel_midjourney_model import GptunnelMidjourneyModel
from dotenv import load_dotenv
from PIL import Image
import numpy as np
import os


load_dotenv()
model = GptunnelMidjourneyModel(os.getenv("GPTUNNEL_API_KEY"), os.getenv("IMGBB_API_KEY"))

reference_image = np.array(Image.open(r"D:\Projects\visage\data\images\Kirill.jpg"))
generated_image = model.generate_image("A angel flying in the sky", reference_image)

Image.fromarray(generated_image).save("tmp/test_output_image2.png")
