
import requests
from requests import ConnectionError 
from tests.TestServer import TestServer
from time import sleep
from logging import info

test = TestServer()

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    info("Start Server")
    
    

def test_getModels():
    """
    Test get models
    """
    info("Start Server")
    test.startServer()
    sleep(5)
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



def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    
   