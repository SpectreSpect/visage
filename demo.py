from src.models.image_generation.gptunnel_midjourney_api import GptunnelMidjourneyApi
from src.models.face_swapping.gptunnel_faceswap_api import GptunnelFaceswapApi
from dotenv import load_dotenv
import os


load_dotenv()


if __name__ == "__main__":
    api_key = os.getenv("GPTUNNEL_API_KEY")
    image_path = r"data\images\Kirill.jpg"
    prompt = "A full-body portrait of a cyberpunk man standing straight, looking directly into the camera. He wears a futuristic plaid shirt with neon-threaded patterns and high-tech details, paired with rugged cyber-enhanced jeans. His face has subtle cybernetic implants, and neon lights reflect in his intense gaze. The background features a vibrant, dystopian cityscape with holographic billboards and glowing skyscrapers. Cinematic lighting, ultra-realistic details, high contrast, 4K."

    midjourney_model = GptunnelMidjourneyApi(api_key, "a54c25d06453ad529ec313c5fc33c650")
    faceswap_model = GptunnelFaceswapApi(api_key)
    
    image_path = midjourney_model.generate_image(prompt, image_path)
    result_image_path = faceswap_model.swap_faces(image_path, image_path)

    print(result_image_path)