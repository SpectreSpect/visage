from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from PIL import Image, UnidentifiedImageError
import io
import uuid
import os
from src.models.image_generation.gptunnel_midjourney_api import GptunnelMidjourneyApi
from src.models.face_swapping.gptunnel_faceswap_api import GptunnelFaceswapApi
from dotenv import load_dotenv
import logging


load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.FileHandler("logs/app.log"),  # Write logs to file
        logging.StreamHandler()  # Also print logs to console
    ]
)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("starlette").setLevel(logging.WARNING)

debug = os.getenv("DEBUG", "False").lower() == "true"

gptunnel_api_key = os.getenv("GPTUNNEL_API_KEY")
imgbb_api_key = os.getenv("IMGBB_API_KEY")

sent_reference_image_dir = "data/images/sent_reference_images"
generated_image_dir = "data/images/generated_images"


os.makedirs(sent_reference_image_dir, exist_ok=True)
os.makedirs(generated_image_dir, exist_ok=True)

# image_path = r"data\images\Kirill.jpg"
# prompt = "A full-body portrait of a cyberpunk man standing straight, looking directly into the camera. He wears a futuristic plaid shirt with neon-threaded patterns and high-tech details, paired with rugged cyber-enhanced jeans. His face has subtle cybernetic implants, and neon lights reflect in his intense gaze. The background features a vibrant, dystopian cityscape with holographic billboards and glowing skyscrapers. Cinematic lighting, ultra-realistic details, high contrast, 4K."

midjourney_model = GptunnelMidjourneyApi(gptunnel_api_key, imgbb_api_key)
faceswap_model = GptunnelFaceswapApi(gptunnel_api_key)

app = FastAPI()

async def read_uploaded_image(image):
    """Reads and validates an uploaded image file."""
    try:
        reference_image_bytes = await image.read()
        reference_image = Image.open(io.BytesIO(reference_image_bytes))
        reference_image.verify()  # Check if the image is corrupted
        reference_image = Image.open(io.BytesIO(reference_image_bytes))  # Reload after verify

        return reference_image  # Successfully loaded image

    except UnidentifiedImageError as e:
        error_msg = "Uploaded file is not a valid image format."
    except OSError as e:
        error_msg = f"Error reading image: {e}"
    except Exception as e:
        error_msg = f"Unexpected error: {e}"

    if debug:
        raise RuntimeError(error_msg)
    else:
        logging.error(error_msg)
        return None


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.post("/generate")
async def generate(prompt: str = Form(...), image: UploadFile = File(...)):
    """
    Accepts an image file and a text prompt, processes them, 
    and returns a generated image.
    """
    logging.info(f"Received a request to generate an image with the prompt: {prompt}")

    # reference_image = await read_uploaded_image(image)

    # Read the uploaded image
    reference_image_bytes = await image.read()
    reference_image = Image.open(io.BytesIO(reference_image_bytes))

    reference_image_name = f"{uuid.uuid4().hex}.jpg"
    reference_image_path = os.path.join(sent_reference_image_dir, reference_image_name)
    reference_image.save(reference_image_path)

    generated_image_path = midjourney_model.generate_image(prompt, reference_image_path, save_dir=generated_image_dir)
    if generated_image_path is None:
        error_msg = "Midjourney failed to generate the image"
        logging.error(error_msg)
        return HTTPException(status_code=500, detail=error_msg)
    result_image_path = faceswap_model.swap_faces(generated_image_path, reference_image_path, save_dir=generated_image_dir)

    return FileResponse(result_image_path, media_type="image/png")