from concurrent.futures import ThreadPoolExecutor, Future
from typing import Callable, List

from huggingface_hub.utils import RepositoryNotFoundError
from transformers import AutoModel
from huggingface_hub import HfApi

from llmserver.core.ServiceProvider import ServiceProvider
from llmserver.models.HuggingFaceModel import HuggingFaceLLModel
from llmserver.models.interfaces import Model
from llmserver.utils.logger import info, error


class HFModelDownloader:
    def __init__(self, cache_dir: str = None, max_workers: int = 1):
        self._futures: List[Future] = list()
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self.download_dir = cache_dir

    def download_model(self, name: str, callback: Callable[[str], None],
                       error_callback: Callable[[str], None] = lambda name: ()):
        try:
            self._futures.append(self._executor.submit(
                self.__download_model,
                name=name,
                cache_dir=self.download_dir,
                callback=callback
            ))
            info(self.__class__.__name__, f"Added model {name} to download queue!")
        except Exception as e:
            error_callback(name)
            error(self.__class__.__name__, f"Couldn't queue model {name} to download:\n{e}")

    def __download_model(self, name: str, cache_dir=None, callback: Callable[[str], None] = lambda: {}):
        try:
            AutoModel.from_pretrained(name, cache_dir=cache_dir)
            callback(name)
            info(self.__class__.__name__, f"Model {name} download finished!")
        except ValueError as e:
            error(self.__class__.__name__, f"Can't download model {name} because:\n{e}")

    def stop_service(self):
        if self._executor is not None:
            self._executor.shutdown(wait=False, cancel_futures=True)

    def __del__(self):
        self.stop_service()
        del self._executor


class HuggingFaceModelRepository(object):

    def __init__(self, model_downloader: HFModelDownloader):
        self.__downloader = model_downloader
        self.__models_queue: List[str] = list()

    @property
    def queue(self):
        return self.__models_queue.copy()

    def queueModelDownload(self, model: str, callback: Callable[[Model], None]):
        """
        Downloads Model from HuggingFace Repository
        """
        if self.checkModelExist(model) and model not in self.__models_queue:
            self.__models_queue.append(model)
            self.__downloader.download_model(
                name=model,
                callback=lambda name: callback(HuggingFaceLLModel(name=name)),
                error_callback=lambda name: self.__models_queue.remove(name)
            )

    @classmethod
    def checkModelExist(cls, model: str) -> bool:
        try:
            hf_api = HfApi()
            hf_api.model_info(model)
            return True
        except RepositoryNotFoundError as e:
            return False
