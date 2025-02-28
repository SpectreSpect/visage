from abc import ABC
import requests
import time
import os


class BaseApiClient(ABC):
    """Base API client that handles requests, retries, and errors."""
    
    def __init__(self, base_url, api_key, retries=3, backoff=2):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.retries = retries
        self.backoff = backoff
        self.session = requests.Session()

    def request(self, endpoint, method="POST", data=None, params=None, files=None, return_type="json", timeout=10):
        """Handles API requests with retries, error handling, and flexible response types."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return_types = {
            'json': lambda r: r.json(),
            'text': lambda r: r.text,
            'content': lambda r: r.content,
            'response': lambda r: r
        }

        if return_type not in return_types:
            valid_types = ", ".join(return_types.keys())
            raise ValueError(f"Invalid return_type. It should be either one of these: {valid_types}")

        for attempt in range(self.retries):
            try:
                response = self.session.request(
                    method, url, json=data, params=params, files=files, timeout=timeout
                )
                response.raise_for_status()
                return return_types[return_type](response)

            except requests.Timeout:
                if attempt == self.retries - 1:
                    raise TimeoutError(f"Request timed out after {self.retries} retries: {url}")
            except requests.RequestException as e:
                if attempt == self.retries - 1:
                    raise RuntimeError(f"API request failed after {self.retries} retries: {url}. Error: {e}")
            except Exception as e:
                if attempt == self.retries - 1:
                    raise RuntimeError(f"Unexpected error in API request after {self.retries} retries: {url}. Error: {e}")
            
            if attempt < self.retries - 1:
                time.sleep(min(self.backoff * (2 ** attempt), 10))
        
        raise RuntimeError(f"Final attempt failed after {self.retries} retries. API request could not be completed: {url}")
