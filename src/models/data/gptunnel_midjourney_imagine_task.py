from src.models.data.gptunnel_task import GptunnelTask
import requests
import logging

class GptunnelMidjourneyImagineTask(GptunnelTask):

    def __init__(self, index: str, api_key: str):
        super().__init__(index, api_key)
        self.url = "https://gptunnel.ru/v1/midjourney/result"
    
    def get_status(self) -> str:
        url = "https://gptunnel.ru/v1/midjourney/result"
        return self._get_gptunnel_status(url, {"taskId": self.index})
        # headers = {
        #     "Authorization": self.api_key
        # }

        # try:
        #     response = requests.get(url + "?taskId=" + self.index, headers=headers)
        #     response.raise_for_status()

        #     return response.json()["status"]
        # except requests.exceptions.RequestException as e:
        #     error_msg = f"Error getting task status: {e}"
        # except requests.Timeout:
        #     error_msg = "Request timed out while contacting Midjourney API"
        # except requests.RequestException as e:
        #     error_msg = f"Midjourney API request failed: {str(e)}"
        # except ValueError:
        #     error_msg = "Invalid JSON response from Midjourney API"
        # except KeyError as e:
        #     error_msg = f"Key not found in the response: {str(e)}"
        # except Exception as e:
        #     error_msg = f"Unexpected error: {str(e)}"
        
        # if self.debug:
        #     raise RuntimeError(error_msg)
        # else:
        #     logging.error(error_msg)
        #     return None

    # def get_result(self):
    #     url = "https://gptunnel.ru/v1/midjourney/result"
    #     headers = {
    #         "Authorization": self.api_key
    #     }

    #     response = requests.get(url + "?taskId=" + self.index, headers=headers)

    #     return response.json()["result"]
    
    def get_result(self):
        url = "https://gptunnel.ru/v1/midjourney/result"
        json_response = self._get_gptunnel_result(url, {"taskId": self.index})

        if "result" not in json_response:
            error_msg = "Result not found in the response"
            
            if self.debug:
                raise RuntimeError(error_msg)
            else:
                logging.error(error_msg)
                return None


        # headers = {
        #     "Authorization": self.api_key
        # }

        # response = requests.get(url + "?taskId=" + self.index, headers=headers)

        return json_response["result"]