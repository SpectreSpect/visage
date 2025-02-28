from src.models.image_generation.gptunnel_midjourney_model import GptunnelMidjourneyModel
from dotenv import load_dotenv
from PIL import Image
import os


load_dotenv()
model = GptunnelMidjourneyModel(os.getenv("GPTUNNEL_API_KEY"))
image = model.generate_image("A angel flying in the sky")

Image.fromarray(image).save("tmp/test_output_image.png")
