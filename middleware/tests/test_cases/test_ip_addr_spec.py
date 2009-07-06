import unittest
# Hack to get to ip_addr_filter.pyx
import sys
sys.path = [ "../" ] + sys.path
from ip_addr_filter import IPAddressMiddleWare

class TestIPAddressSpec(unittest.TestCase):

    def test01_simple(self):
        """Simple test
        """
        self.assertEqual( 1, 1 )
        #self.assertRaises( );

def suite():
    s = unittest.TestSuite()
    s.addTest( unittest.makeSuite( TestIPAddressSpec ) )
    return s

def run(verbosity=2):
    """Test for IP address settings.
    """
    unittest.TextTestRunner( verbosity=verbosity ).run( suite() )
