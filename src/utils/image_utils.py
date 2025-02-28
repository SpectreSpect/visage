import base64
import mimetypes
import numpy as np
from io import BytesIO
from PIL import Image

def image_to_base64(image: np.ndarray, image_format="PNG") -> str:
    """
    Converts a NumPy ndarray image to a Base64-encoded string.
    
    :param image: Image as a NumPy array.
    :param image_format: Format to encode image (e.g., "PNG", "JPEG").
    :return: Base64 string with MIME type.
    """
    # Convert NumPy array to PIL Image
    pil_image = Image.fromarray(image)  

    # Save the image to a buffer
    buffer = BytesIO()
    pil_image.save(buffer, format=image_format)
    mime_type = f"image/{image_format.lower()}"

    # Encode to Base64
    base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:{mime_type};base64,{base64_str}"
