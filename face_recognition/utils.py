from .recognizer import Face


def calculate_bbox_area(bbox: tuple[tuple[int, int], tuple[int, int]]):
    (x1, y1), (x2, y2) = bbox
    return (x2 - x1) * (y2 - y1)


def get_max_bbox(faces: list[Face]):
    max_area = 0
    max_face = None
    for face in faces:
        area = calculate_bbox_area(face.bbox)
        if area > max_area:
            max_area = area
            max_face = face
    return max_face
