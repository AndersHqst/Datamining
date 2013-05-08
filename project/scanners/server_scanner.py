from HTMLParser import HTMLParser
from utils.preprocessing_helper import index_of_discrete_bin

"""Find server type from the HTTP header."""

class ServerStopException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__(*args, **kwargs)

def bins():
    return ['NGINX', 'MICROSOFT-IIS', 'MEEBOX', 'APACHE', 'LWS', 'GNOL', 'LITESPEED', 'LIGHTTPD', 'CONCEALED BY JUNIPER NETWORKS DX', 'IBE', 'GWS', 'OVERSEE TURING', 'WP ENGINE', 'IBM_HTTP_SERVER', 'ORACLE', 'ZOPE', 'DEMANDWARE ECOMMERCE SERVER', 'LOTUS-DOMINO', 'MARVIN', 'VARNISH', 'MOJOLICIOUS', 'GSE', 'UNKNOWN']

def server_scanner(website):
    server = ''
    if website.headers.has_key('server'):
        server = website.headers['server'].strip().upper()
    elif website.headers.has_key('Server'):
        server = website.headers['Server'].strip().upper()
    index = index_of_discrete_bin(bins(), server)
    if index == -1:
        index = bins().index('UNKNOWN')
    else:
        pass
    return 'server', index