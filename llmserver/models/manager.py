import types
from typing import List, KeysView

from llmserver.models.interfaces import Model
from llmserver.repository.ModelsRepository import ModelsRepository


class ModelScheduler(object):
    _queue: List[Model] = list()
    _maxModels = 1

    def __init__(self, max_models: int = 1):
        self._maxModels = max_models

    def isModelReady(self, model: Model) -> bool:
        return model in self._queue

    def scheduleModel(self, model: Model):
        if model in self._queue:
            return

        while len(self._queue) >= self._maxModels:
            self._queue.pop(0).unloadModel()

        model.loadModel()
        self._queue.append(model)

    def clearQueue(self):
        [it.unloadModel() for it in self._queue]
        self._queue.clear()


class ModelManager(object):
    _modelsRepository: ModelsRepository
    _scheduler = ModelScheduler(max_models=1)

    @property
    def models(self) -> KeysView[str]:
        return self._modelsRepository.models.keys()

    def __init__(self, repository: ModelsRepository):
        self._modelsRepository = repository

    @property
    def scheduler(self) -> ModelScheduler:
        return self._scheduler

    def schedule(self, name: str):
        self._scheduler.scheduleModel(self.getModel(name))

    def _changeModel(self, name: str):
        if name not in self.models:
            raise ValueError("model is not in dictionary")

        self._scheduler.scheduleModel(self.getModel(name))

    def getModel(self, name: str) -> Model:
        return self._modelsRepository.getModel(name)

    def addModel(self, model: Model):
        self._modelsRepository.addModel(model)
