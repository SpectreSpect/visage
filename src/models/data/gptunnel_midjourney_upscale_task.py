from src.models.data.gptunnel_task import GptunnelTask
import requests

class GptunnelMidjourneyUpscaleTask(GptunnelTask):

    def __init__(self, index: str, api_key: str):
        super().__init__(index, api_key)
        self.url = "https://gptunnel.ru/v1/midjourney/result"
    
    def get_status(self) -> str:
        url = "https://gptunnel.ru/v1/midjourney/result"
        headers = {
            "Authorization": self.api_key
        }

        response = requests.get(url + "?taskId=" + self.index, headers=headers)

        return response.json()["status"]


    def get_result(self):
        url = "https://gptunnel.ru/v1/midjourney/result"
        headers = {
            "Authorization": self.api_key
        }

        response = requests.get(url + "?taskId=" + self.index, headers=headers)

        return response.json()["result"]