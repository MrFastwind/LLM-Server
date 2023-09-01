from llmserver.core.ApiServer import ApiServer
from multiprocessing import Process

class TestServer(object):
    
    process: Process
    
    def startServer(self):
        self.process = Process(target=TestServer.__runServer)
        self.process.start()
    
    @classmethod
    def __runServer(cls):
        apiserver = ApiServer()
        apiserver.startServer()
    
    def stopServer(self):
        self.process.terminate()