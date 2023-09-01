
import requests
from requests import ConnectionError 
from tests.TestServer import TestServer
from time import sleep
from logging import info

from llmserver.models.manager import ModelManager

def test_loadModel():
    """
    Test load of model
    """

    manager = ModelManager()
    
    manager.
    try:
        # response = requests.get(
        #    url="http://127.0.0.1:8002/models", 
        #    timeout=3000
        # )
        pass
    except Exception as e:
        raise e
    finally:
        test.stopServer()
    
    #assert response.status_code == 200
