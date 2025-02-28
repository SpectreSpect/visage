from src.models.base_model import BaseModel
import numpy as np
import os

class ImageGenModel(BaseModel):
	def __init__(self):
		super().__init__()

	def generate_image(self, prompt: str, reference_image: np.ndarray = None) -> np.ndarray:
		pass