import os, re
from optparse import OptionParser
import urllib, urllib2, urlparse
import MultipartPostHandler, urllib2, cookielib

PATH = '.'
USER = 'niels'
PASSWORD = 'niels'
#URL = 'http://localhost:8000/'
URL = 'http://imagedb.ciboe.webfactional.com/'
ADMIN_PATH = '/admin/files/image/add/'
LOGIN_PATH = '/login/'

category_mapping = {'A':'location', 'B':'events', 'C':'graphics'}

def handle_file(opener, dirname, name):

#<QueryDict: {u'is_public': [u'on'], u'_save': [u'Save'], u'locations': [u'1', u'2']}> <MultiValueDict: {u'image': [<InMemoryUploadedFile: VOR10298.jpg (image/jpeg)>]}>

    categories = re.findall(r'[A-Z][0-9]{2}',dirname)
    image = os.path.join(dirname, name)

    params = { "username" : USER, "password" : PASSWORD, 'is_public': 'on', '_save': 'Save',
             "image" : open(image, "rb") }
    f = opener.open(urlparse.urljoin(URL, ADMIN_PATH), params)
    #print f.read()

    #c = [(category_mapping[category[0]], [int(category[1:3])]) for category in categories]
    #data.update(dict(c))

def visit(arg, dirname, names):
    # handle each file 
    for name in names:
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
    #f = opener.open('http://imagedb.ciboe.webfactional.com/login/', params)
    f = opener.open(urlparse.urljoin(url, LOGIN_PATH), params)
    data = f.read()
    f.close()

    # walk the dir tree
    os.path.walk(path, visit, opener)

if __name__ == "__main__":
    main()
