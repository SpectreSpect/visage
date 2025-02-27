from src.models.data.task import Task
import logging

class GptunnelTask(Task):

    def __init__(self, index: str, api_key: str):
        super().__init__()
        self.index = index
        self.api_key = api_key
    
    def _get_gptunnel_status(self, url: str, params: dict) -> str:
        url = "https://gptunnel.ru/v1/midjourney/result"

        json_response = self._get_gptunnel_result(url, params)

        if "status" not in json_response:
            error_msg = "Status not found in the response"
            
            if self.debug:
                raise RuntimeError(error_msg)
            else:
                logging.error(error_msg)
                return None

        return json_response["status"]
    
    def _get_gptunnel_result(self, url: str, params: dict) -> dict:
        json_response = self._make_json_get_request(url, headers={"Authorization": self.api_key}, params=params)
        return json_response