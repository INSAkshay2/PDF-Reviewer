from abc import ABC, abstractmethod

import numpy as np


class EmbeddingService(ABC):
    @property
    @abstractmethod
    def dimension(self) -> int:
        ...

    @abstractmethod
    def embed_documents(self, texts: list[str]) -> np.ndarray:
        ...

    @abstractmethod
    def embed_query(self, query: str) -> np.ndarray:
        ...
