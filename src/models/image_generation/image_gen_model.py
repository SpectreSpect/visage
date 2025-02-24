from abc import ABC
import numpy as np

class ImageGenModel(ABC):
	def __init__(self):
		self.output_dir = "output"
		

	def generate_image(self, prompt: str) -> np.ndarray:
		pass