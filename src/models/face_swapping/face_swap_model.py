from src.models.base_model import BaseModel
import numpy as np

class FaceSwapModel(BaseModel):
	def __init__(self):
		pass

	def swap_faces(self, source_image: np.ndarray, face_image: np.ndarray) -> np.ndarray:
		pass