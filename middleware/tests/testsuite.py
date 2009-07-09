import unittest
from test_cases import test_ip_addr_spec

test_suites = [
    test_ip_addr_spec.suite(),
    ]

def suite():
    """Returns suite of all the test test_cases.
    """
    s = unittest.TestSuite()
    map( s.addTest, test_suites )
    return s

def run(verbosity=1):
    """Runs the tests.
    """
    unittest.TextTestRunner( verbosity=verbosity ).run( suite() )
