from abc import ABC
import os
import requests
import logging


class Task(ABC):
    def __init__(self):
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
    
    def _make_json_get_request(self, url: str, headers: dict = None, params: dict = None):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()

            return response.json()
        except requests.Timeout:
            error_msg = "Request timed out while contacting making a task request"
        except requests.RequestException as e:
            error_msg = f"Task request failed: {str(e)}"
        except ValueError:
            error_msg = "Invalid JSON response from a task request"
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
        
        if self.debug:
            raise RuntimeError(error_msg)
        else:
            logging.error(error_msg)
            return None

    def get_status(self) -> str:
        pass

    def get_percent(self) -> int:
        pass

    def get_result(self):
        pass