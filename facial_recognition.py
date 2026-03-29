import io

import cv2
import numpy as np
from PIL import Image

from face_recognition import FaceDB, Recognizer, get_max_bbox

face_db = FaceDB("data")
recognizer = Recognizer()


def register_face(img_data: bytes, username: str):
    img_arr = np.array(Image.open(io.BytesIO(img_data)))
    faces = recognizer.recognize(img_arr)

    if not faces:
        raise ValueError("No face detected")

    face_db.add(username, get_max_bbox(faces).embedding)


def detect_face(img_data: bytes):
    img_arr = np.array(Image.open(io.BytesIO(img_data)))
    faces = recognizer.recognize(img_arr)

    if not faces:
        _, img_encoded = cv2.imencode(".jpg", img_arr)
        return img_encoded.tobytes(), None

    max_face = get_max_bbox(faces)
    username, _ = face_db.query(max_face.embedding)

    (x1, y1), (x2, y2) = max_face.bbox
    cv2.rectangle(img_arr, (x1, y1), (x2, y2), (0, 255, 0), 2)
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
    _, img_encoded = cv2.imencode(".jpg", img_arr)

    return img_encoded.tobytes(), username


def remove_face(username: str): ...
