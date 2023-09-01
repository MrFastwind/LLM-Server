from llmserver.core.ApiServer import ApiServer
from llmserver.core.ServiceProvider import SingletonServiceProvider
from llmserver.models.manager import ModelManager
from llmserver.repository.HuggingFaceModelRepository import HuggingFaceModelRepository, HFModelDownloader
from llmserver.repository.ModelsRepository import ModelsRepository
from llmserver.utils.configuration.ConfigurationLoader import ConfigurationLoader
from llmserver.utils.configuration.HuggingFaceConfiguration import HuggingFaceConfig


def loadRouters(apiServer: ApiServer):
    from llmserver.routers.models import modelRouter
    apiServer.addRouter(modelRouter)


def main():
    config_loader = ConfigurationLoader("./config.yaml").load_config()

    config = config_loader.configure(HuggingFaceConfig)

    provider = SingletonServiceProvider.get_instance()
    provider.register_singleton(HFModelDownloader, HFModelDownloader(
        cache_dir=config.cache_path,
        max_workers=1
    ))
    provider.register_singleton(HuggingFaceModelRepository)
    provider.register_singleton(ModelsRepository)
    provider.register_singleton(ModelManager)

    apiServer = ApiServer()
    loadRouters(apiServer)

    apiServer.startServer()


if __name__ == "__main__":
    main()
