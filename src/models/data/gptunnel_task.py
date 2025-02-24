from src.models.data.task import Task

class GptunnelTask(Task):

    def __init__(self, index: str, api_key: str):
        self.index = index
        self.api_key = api_key