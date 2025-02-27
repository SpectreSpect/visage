from abc import ABC
import numpy as np

class FaceSwapModel(ABC):
	def __init__(self):
		pass

	def swap_faces(self, img1_path: str, img2_path: str, save_dir: str = "output") -> str:
		pass