from src.models.data.gptunnel_task import GptunnelTask
import requests
import logging

class GptunnelFaceswaptask(GptunnelTask):

    def __init__(self, index: str, api_key: str):
        super().__init__(index, api_key)
    
    def get_status(self) -> str:
        url = "https://gptunnel.ru/v1/faceswap/result"
        return self._get_gptunnel_status(url, {"taskId": self.index})

    def get_result(self):
        url = "https://gptunnel.ru/v1/faceswap/result"
        json_response = self._get_gptunnel_result(url, {"taskId": self.index})

        if "result" not in json_response:
            error_msg = "Result not found in the response"
            
            if self.debug:
                raise RuntimeError(error_msg)
            else:
                logging.error(error_msg)
                return None
        # response = self.get_result_dict()
        return json_response["result"]