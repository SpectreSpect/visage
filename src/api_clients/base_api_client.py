from abc import ABC
import requests
import time
import logging
import os


class BaseApiClient(ABC):
    """Base API client that handles requests, retries, and errors."""
    
    def __init__(self, base_url, api_key, retries=3, backoff=2):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.retries = retries
        self.backoff = backoff
        self.session = requests.Session()
        self.session.headers.update({"Authorization": self.api_key})

        # Read DEBUG from environment variables (default: False)
        self.debug = os.getenv("DEBUG", "False").lower() == "true"

    def request(self, endpoint, method="POST", data=None, params=None, files=None, return_type="json", timeout=10):
        """Handles API requests with retries, error handling, and flexible response types."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        last_exception = None  # Store the last exception to raise later if needed

        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method, url, json=data, params=params, files=files, timeout=timeout
                )
                response.raise_for_status()
                
                # Handle different response types
                if return_type == "json":
                    return response.json()
                elif return_type == "text":
                    return response.text
                elif return_type == "content":
                    return response.content  # Useful for images/files
                elif return_type == "response":
                    return response  # Full response object
                else:
                    raise ValueError(f"Invalid return_type: {return_type}")

            except requests.Timeout:
                last_exception = RuntimeError(f"Attempt {attempt + 1}: Request timed out (URL: {url})")
            except requests.RequestException as e:
                last_exception = RuntimeError(f"Attempt {attempt + 1}: API request failed (URL: {url}): {e}")
            except Exception as e:
                last_exception = RuntimeError(f"Unexpected error (URL: {url}): {e}")

            logging.warning(str(last_exception))

            # Wait before retrying
            if attempt < self.retries - 1:
                time.sleep(self.backoff * (2 ** attempt))

        # If all attempts failed, log and raise the final error
        final_error_msg = f"Final attempt failed. API request could not be completed: {url}"
        logging.error(final_error_msg)

        if self.debug:
            if last_exception:
                raise last_exception
            raise RuntimeError(final_error_msg)

        return None
