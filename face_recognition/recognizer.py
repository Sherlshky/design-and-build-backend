from dataclasses import dataclass

import numpy as np
from insightface.app import FaceAnalysis


@dataclass
class Face:
    embedding: np.ndarray
    bbox: tuple[tuple[int, int], tuple[int, int]]
    det_score: float


class Recognizer:
    def __init__(self, model_name="buffalo_m", det_size=640, download=True):
        self._app = FaceAnalysis(name=model_name, allowed_modules=["detection", "recognition"], download=download)
        self._app.prepare(ctx_id=0, det_size=(det_size, det_size))

    def recognize(self, img: np.ndarray) -> list[Face]:
        result = self._app.get(img)

        ret = []
        for res in result:
            x1, y1, x2, y2 = map(int, res["bbox"])
            embedding = res["embedding"]
            det_score = res["det_score"]
            ret.append(Face(embedding, ((x1, y1), (x2, y2)), det_score))

        return ret
