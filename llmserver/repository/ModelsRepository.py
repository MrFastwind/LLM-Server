import types
from types import MappingProxyType
from typing import Dict, List

from llmserver.models.HuggingFaceModel import HuggingFaceLLModel
from llmserver.models.interfaces import Model
from llmserver.repository.HuggingFaceModelRepository import HuggingFaceModelRepository


class ModelsRepository(object):

    def __init__(self, repository: HuggingFaceModelRepository):
        self.hfRepository: HuggingFaceModelRepository = repository

    _models: Dict[str, Model] = {}

    def removeModel(self, name: str):
        if name in self._models:
            del self._models[name]

    def retrieveHuggingFaceModel(self, model: str):
        if model in self.hfRepository.queue or model in self._models:
            return
        self.hfRepository.queueModelDownload(
            model=model,
            callback=lambda generated_model: self.__add_downloaded_model(generated_model)
        )

    def __add_downloaded_model(self, model: HuggingFaceLLModel):
        self.addModel(model)

    def addModel(self, model: Model):
        self._models[model.name] = model

    @property
    def models(self) -> MappingProxyType[str, Model]:
        return types.MappingProxyType(self._models)

    def getModel(self, name: str) -> Model:
        return self._models[name]
