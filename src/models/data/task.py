from abc import ABC


class Task(ABC):
	def __init__(self):
		pass

	def get_status(self) -> str:
		pass

	def get_percent(self) -> int:
		pass

	def get_result(self):
		pass