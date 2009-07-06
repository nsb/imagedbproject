import os, logging

logfile = os.path.join( os.path.dirname( __file__ ), 'log',
                        'test_results.log' )
logging.basicConfig( level=logging.DEBUG,
                     format = '%(asctime)s %(levelname)s %(message)s',
                     filename = logfile,
                     filemode = 'w' )
