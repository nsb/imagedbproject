# Copyright 2008 - 2009, Niels Sandholt Busch <niels.busch@gmail.com>. All rights reserved.

import os, re
from optparse import OptionParser
import urllib, urllib2, urlparse
import MultipartPostHandler, urllib2

PATH = '.'
USER = 'niels'
PASSWORD = 'niels'
#URL = 'http://localhost:8000/'
URL = 'http://imagedb.ciboe.dk/'
ADMIN_PATH = '/admin/files/image/add/'
LOGIN_PATH = '/login/'

category_mapping = {
    'A':'locations',
    'B':'fields',
    'C':'installations',
    'D':'people',
    'E':'hse',
    'F':'events',
    'G':'communcations',
    'H':'archives',}

def handle_file(opener, dirname, name):

    categories = re.findall(r'[A-Z][0-9]{2}',dirname)
    image = os.path.join(dirname, name)

    print 'uploading image %s with categories %s...' % (name, categories),

    params = [('is_public', 'on'), ('_save', 'Save'), ("image", open(image, "rb")) ]
    params += [(category_mapping[category[0]], str(int(category[1:3]))) for category in categories]
    f = opener.open(urlparse.urljoin(URL, ADMIN_PATH), params)
    data = f.read()
    f.close()

    print 'done'    

def visit(arg, dirname, names):
    # handle each file
    for index, name in enumerate(names):
        if name.startswith('.'):
            del names[index]
        else:
            if os.path.isfile(os.path.join(dirname, name)):
                handle_file(arg, dirname, name)

def main():
    # options
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="path",
                      help="path to root dir", metavar="PATH")
    parser.add_option("-u", "--user", dest="user",
                      help="username")
    parser.add_option("-p", "--password", dest="password",
                      help="password")
    parser.add_option("-l", "--url", dest="url",
                      help="host url")

    (options, args) = parser.parse_args()

    path = options.path or PATH
    user = options.user or USER
    password = options.password or PASSWORD
    url = options.url or URL

    # init url lib with cookie based auth handler
    opener = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(), MultipartPostHandler.MultipartPostHandler)
    urllib2.install_opener(opener)

    # do login
    params = urllib.urlencode(dict(username=user, password=password))
    f = opener.open(urlparse.urljoin(url, LOGIN_PATH), params)
    data = f.read()
    f.close()

    # walk the dir tree
    os.path.walk(path, visit, opener)

if __name__ == "__main__":
    main()
