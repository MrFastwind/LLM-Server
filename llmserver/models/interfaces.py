from abc import ABC, abstractmethod


class Model(ABC):
    name: str

    @abstractmethod
    def loadModel(self):
        raise NotImplementedError()

    @abstractmethod
    def unloadModel(self):
        raise NotImplementedError()

    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError()
