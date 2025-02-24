from src.models.data.gptunnel_task import GptunnelTask
import requests

class GptunnelFaceswaptask(GptunnelTask):

    def __init__(self, index: str, api_key: str):
        super().__init__(index, api_key)
        self.url = "https://gptunnel.ru/v1/faceswap/result"
    
    def get_result_dict(self) -> dict:
        headers = {
            "Authorization": self.api_key
        }

        response = requests.get(self.url + "?taskId=" + self.index, headers=headers)
        return response.json()
    
    def get_status(self) -> str:
        response = self.get_result_dict()
        return response["status"]

    def get_result(self):
        response = self.get_result_dict()
        return response["result"]