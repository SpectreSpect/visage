from abc import ABC
import numpy as np
import os

class ImageGenModel(ABC):
	def __init__(self):
		self.debug = os.getenv("DEBUG", "False").lower() == "true"

	def generate_image(self, prompt: str, source_image_path: str = None, save_dir: str = "output") -> str:
		pass