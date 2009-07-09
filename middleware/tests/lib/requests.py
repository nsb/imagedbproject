import httplib, urllib, sys
#from validators import request_succeeded
from conf import settings
from logger import logging

def http_request(url):
    """ Sends an HTTP GET request and returns the received response.
    """
    response = False
    conn = httplib.HTTPConnection( settings.DOMAIN, settings.PORT )
    conn.putrequest( "GET", url )
    
    try:
        conn.endheaders()
    except:
        logging.debug( 'Failed connecting to server.' )
        logging.debug( sys.exc_info() )
    else:
        response = conn.getresponse()
        conn.close()
    
    return response

