from abc import ABC
import numpy as np

class ImageGenModel(ABC):
	def __init__(self):
		self.output_dir = "output"
		

	def generate_image(self, prompt: str, source_image_path: str = None) -> str:
		pass