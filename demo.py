from src.models.image_generation.gptunnel_midjourney_api import GptunnelMidjourneyApi
from src.models.face_swapping.gptunnel_faceswap_api import GptunnelFaceswapApi
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    api_key = os.getenv("GPTUNNEL_API_KEY")
    image_path = ""
    prompt = "Galactic human. This being is unfathomable. He's made of stars and nebulae, yet his face is clearly visible. The image is very colorful."

    midjourney_model = GptunnelMidjourneyApi(api_key, "a54c25d06453ad529ec313c5fc33c650")
    faceswap_model = GptunnelFaceswapApi(api_key)
    
    image_path = midjourney_model.generate_image(prompt, image_path)
    result_image_path = faceswap_model.swap_faces(image_path, image_path)

    print(result_image_path)