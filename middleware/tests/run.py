import env, testsuite
#from conf import settings
from lib import requests

def init():
    """Performs all the initialization prior executing unit tests.
    
    Returns True on success, else False.
    """
    status = True #False
    #status = requests.http_request( settings.LOAD_DATA_URL )
    #print settings.LOAD_DATA_URL
    return status

def cleanup():
    """Performs all post unit test clean-ups.
    
    Returns True on success, else False.
    """
    status = True #False
    #status = requests.http_request( settings.CLEAR_DATA_URL )
    return status

if __name__ == '__main__':
    if init():
        try:
            testsuite.run()
        except Exception, e:
            print 'testsuite.run: An exception occurred:\n' + str( e )
        finally:
            cleanup()
    else:
        print 'testsuite: Failure in initialisation prior to tests'

