from fastapi import FastAPI, APIRouter
from llmserver.core.ServiceProvider import SingletonServiceProvider, ServiceProvider
import uvicorn

from llmserver.models.manager import ModelManager


class ApiServer(object):
    app: FastAPI = None
    provider: SingletonServiceProvider = None

    def __init__(self, host: str = "0.0.0.0", port: int = 8002):
        self.host = host
        self.port = port
        self.app = FastAPI()
        self.setProvider(SingletonServiceProvider.get_instance())

    def addRouter(self, router: APIRouter):
        self.app.include_router(router)

    def setProvider(self, provider: SingletonServiceProvider):
        self.provider = provider

    def startServer(self):
        uvicorn.run(self.app, host=self.host, port=self.port)
