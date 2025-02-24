from abc import ABC
import numpy as np

class FaceSwapModel(ABC):
	def __init__(self):
		self.output_dir = "output"

	def swap_faces(self, img1_path: str, img2_path: str) -> np.ndarray:
		pass