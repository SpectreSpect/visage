from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from PIL import Image, UnidentifiedImageError
from src.models.image_generation.gptunnel_midjourney_model import GptunnelMidjourneyModel
from src.models.face_swapping.gptunnel_faceswap_model import GptunnelFaceSwapModel
from dotenv import load_dotenv
from PIL import Image
import logging
import numpy as np
import uuid
import os
import io


load_dotenv()

logs_dir = "logs"
reference_upload_dir = os.path.join(logs_dir, "uploads/reference")
generated_upload_dir = os.path.join(logs_dir, "uploads/generated")
face_swapped_upload_dir = os.path.join(logs_dir, "uploads/face_swapped")

os.makedirs(logs_dir, exist_ok=True)
os.makedirs(reference_upload_dir, exist_ok=True)
os.makedirs(generated_upload_dir, exist_ok=True)
os.makedirs(face_swapped_upload_dir, exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"), 
        logging.StreamHandler()
    ]
)

for lib in ["urllib3", "requests", "httpx", "uvicorn", "starlette", "multipart", "httptools", "formparse"]:
    logging.getLogger(lib).setLevel(logging.WARNING)


debug = os.getenv("DEBUG", "False").lower() == "true"

gptunnel_api_key = os.getenv("GPTUNNEL_API_KEY")
imgbb_api_key = os.getenv("IMGBB_API_KEY")



image_gen_model = GptunnelMidjourneyModel(gptunnel_api_key, imgbb_api_key)
faceswap_model = GptunnelFaceSwapModel(gptunnel_api_key)

app = FastAPI()


async def read_uploaded_image(image: UploadFile) -> np.ndarray:
    """Reads, validates, and converts an uploaded image to a NumPy array."""
    try:
        reference_image_bytes = await image.read()
        image_stream = io.BytesIO(reference_image_bytes)

        reference_image = Image.open(image_stream)
        reference_image.verify()  # ✅ Checks if image is valid

        image_stream.seek(0)  # Reset file pointer
        reference_image = Image.open(image_stream).convert("RGB")  # Ensure consistency
        return np.array(reference_image)  # ✅ Convert to NumPy array
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image format.")
    except OSError as e:
        raise HTTPException(status_code=400, detail=f"Error reading image: {e}")
    except Exception as e:
        raise e


@app.get("/")
async def read_root():
    return JSONResponse(status_code=200, content={"message": "Welcome to the Visage API!"})


@app.post("/generate")
async def generate(prompt: str = Form(...), image: UploadFile = File(...)):
    """
    Accepts an image file and a text prompt, processes them, 
    and returns a generated image.
    """
    request_id = uuid.uuid4().hex
    logging.info(f"New generation request: {request_id}")

    try:
        reference_image = await read_uploaded_image(image)
        Image.fromarray(reference_image).save(os.path.join(reference_upload_dir, f"{request_id}.png"))

        generated_image = image_gen_model.generate_image(prompt, reference_image)
        Image.fromarray(generated_image).save(os.path.join(generated_upload_dir, f"{request_id}.png"))
    
        face_swapped_image = faceswap_model.swap_faces(generated_image, reference_image)
        Image.fromarray(face_swapped_image).save(os.path.join(face_swapped_upload_dir, f"{request_id}.png"))

        img_io = io.BytesIO()
        Image.fromarray(face_swapped_image).save(img_io, format="PNG")
        img_io.seek(0)

        logging.info(f"Successfully processed request {request_id}")
        return StreamingResponse(img_io, media_type="image/png")
    except Exception as e:
        if debug:
            raise e
        
        logging.exception(f"Image processing failed (request_id={request_id}): {e}")

        error_msg = str(e) if debug else "An internal error occurred."
        return JSONResponse(status_code=500, content={"error": f"Image processing failed: {error_msg}"})