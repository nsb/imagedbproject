from os import system
# Hack to get to middleware.py
import sys
sys.path = [ "../../" ] + sys.path
import unittest
from middleware import IPAddressMiddleware
from netaddr import AddrFormatError

LOCAL_SETTINGS_FILE = '../../settings_local.py'
LOCAL_SETTINGS_FILE_BAK = '../../settings_local.py.bak'

class TestIPAddressSpec(unittest.TestCase):

    def setUp(self):
        system( 'cp ' + LOCAL_SETTINGS_FILE + ' ' + LOCAL_SETTINGS_FILE_BAK )

    def tearDown(self):
        system( 'mv ' + LOCAL_SETTINGS_FILE_BAK + ' ' + LOCAL_SETTINGS_FILE )

    def test01_invalid_ip(self):
        """Test for invalid IPs. An AddFormatError exception should be thrown
        """
#         INVALID_IP = '"192.168.1.256"'
#         system( r"sed 's/\(^SRJ_IP_REG = \)\(.*\)/\1\[" + \
#                     str( INVALID_IP ) + "]/' " + LOCAL_SETTINGS_FILE + \
#                     " > tmp.$$ && cp tmp.$$ " + LOCAL_SETTINGS_FILE )
#         self.assertRaises( Exception, IPAddressMiddleware ) 

    def test02_valid_ip(self):
        """Test for valid IPs.
        """
        try:
            IPAddressMiddleware()
        except Exception, e:
            self.fail( 'Unexpected exception. Error message is:\n' + str(e) )

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite( TestIPAddressSpec ) )
    return s

def run(verbosity=2):
    """Test for IP address settings.
    """
    unittest.TextTestRunner( verbosity=verbosity ).run( suite() )
