import requests
from PIL import Image
from io import BytesIO
import numpy as np

class ImageLoader:
    """Utility class for loading images from URLs into memory as NumPy arrays."""

    @staticmethod
    def load(url: str, timeout: int = 10) -> np.ndarray:
        """
        Loads an image from a URL into memory as a NumPy array.

        :param url: The image URL.
        :param timeout: Maximum time (in seconds) to wait for a response.
        :return: Image as a NumPy array.
        :raises TimeoutError: If the request times out.
        :raises RuntimeError: If the request fails or an unexpected error occurs.
        """
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            return np.array(image)

        except requests.Timeout:
            raise TimeoutError(f"Image loading timed out after {timeout} seconds.")
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to load image from {url}: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while loading image from {url}: {e}")