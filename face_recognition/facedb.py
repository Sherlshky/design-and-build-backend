import uuid
import warnings

import chromadb
import numpy as np


class FaceDB:
    def __init__(self, db_path: str = "data/db"):
        self._client = chromadb.PersistentClient(path=db_path, settings=chromadb
                                                 .Settings(allow_reset=True, anonymized_telemetry=False))
        self._db = self._client.get_or_create_collection("Faces", metadata={"hnsw:space": "cosine"})

    def add(self, name: str, embedding: np.ndarray):
        if self.query(embedding, 0.99)[0] is not None:
            warnings.warn(f"Embedding for {name} already exists in the database")
            return
        if not name:
            return
        face_id = str(uuid.uuid4())
        self._db.add(face_id, embedding.tolist(), metadatas={"name": name})

    def query(self, embedding: np.ndarray, threshold: float = 0.5):
        if not self._db.count():
            return None, 0.0
        result = self._db.query(embedding.tolist(), n_results=1)
        if not result['ids'][0]:
            return None, 0.0
        name, sim = result['metadatas'][0][0]['name'], 1 - result['distances'][0][0]
        if sim < threshold:
            return None, sim
        return name, sim

    def delete(self, embedding: np.ndarray):
        result = self._db.query(embedding.tolist(), n_results=1)
        idx = result['ids'][0]
        if not idx:
            return None
        self._db.delete(idx)
        return result['metadatas'][0][0]['name']

    def clear(self):
        self._client.reset()
        self._db = self._client.get_or_create_collection("Faces", metadata={"hnsw:space": "cosine"})

    def query_all(self) -> dict[str, str]:
        num = self._db.count()
        results = self._db.peek(limit=num)
        names = [metadata['name'] for metadata in results['metadatas']]
        return dict(zip(names, results['ids']))


if __name__ == "__main__":
    db = FaceDB("data/test_db")
    emb = np.ones(10)
    db.add("test", emb)
    print(db.query(emb))
