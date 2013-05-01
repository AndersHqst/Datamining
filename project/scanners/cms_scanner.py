from HTMLParser import HTMLParser
import urllib2
from urlparse import urlparse

"""
    Parse CMS system for a website

    TODO: Use reg ex when searching for a specific string in the raw HTML text.
"""

DOTNETNUKE = 'DOTNETNUKE'
UMBRACO    = 'UMBRACO'
EPISERVER  = 'EPISERVER'
SHAREPOINT = 'SHAREPOINT'
SITECORE   = 'SITECORE'
DYNAMICWEB = 'DYNAMICWEB'
WORDPRESS  = 'WORDPRESS'
TYPO3      = 'TYPO3'
PHPNUKE    = 'PHPNUKE'
DRUPAL     = 'DRUPAL'
JOOMLA     = 'JOOMLA'
UNKNOWN    = 'UNKNOWN'

class CMSHTMLParser(HTMLParser):

    def __init__(self, website):
        HTMLParser.__init__(self)
        self.website = website
        self.cms = 'UNKNOWN'
        self.parsing_script = False

        self.wp_verbs = set(['wp-content', 'wp-include'])

        self.type3_comment_text = ['This website is powered by TYPO3',
        'TYPO3 is a free open source Content Management Framework']


    def feed(self, data):
        """Overrides feed. Some CMS we will just find by searching for a string in the HTML"""
        if data == None or data.isspace():
            print 'CMS parser data was not there'
            raise Exception

        #See if some cms is simply mentioned in the header
        drupal = 'drupal'
        umbraco = 'umbraco'
        for key in self.website.headers.keys():

            #Drupal
            if drupal in self.website.headers[key].lower() or drupal in key.lower():
                self.cms = DRUPAL
                raise Exception

            #Umbraco
            if umbraco in self.website.headers[key].lower() or umbraco in key.lower():
                self.cms = UMBRACO
                raise Exception


        #See if a certain path name occurs
        dnn_path = '/Portals/_default/'
        if dnn_path in self.website.html:
            self.cms = DOTNETNUKE
            raise Exception

        #Umbraco
        umbraco_path = '/umbraco/'
        if umbraco_path in self.website.html:
            self.cms = DOTNETNUKE
            raise Exception

        #Sitecore
        sitecore_content_path = 'sitecore/content/'
        sitecore_util_path = 'http://www.sitecore.net/webutil'
        if sitecore_content_path in self.website.html or sitecore_util_path in self.website.html:
            self.cms = SITECORE
            raise Exception

        HTMLParser.feed(self, data)


    def handle_starttag(self, tag, attrs):
        self.parsing_script = False
        href = next((b for a,b in attrs if a == 'href'), '')
        src = next((b for a,b in attrs if a == 'src'), '')

        #Wordpress
        if href in self.wp_verbs or src in self.wp_verbs:
            self.cms = WORDPRESS
            raise Exception

        #Script
        if tag == 'script':
            self.parsing_script = True
            src = next((b for a,b in attrs if a == 'src'), '')

            #Joomal
            if 'typo3' in src:
                self.cms = TYPO3
                raise Exception

            #Joomla
            if 'joomla' in src:
                self.cms = JOOMLA
                raise Exception

            #DotNetNuke
            if 'dnn.js' in src or 'dnncore.js' in src:
                self.cms = DOTNETNUKE
                raise Exception

            #Sharepoint
            if 'init.js' in src or 'core.js' in src or 'msstring.js' in src:
                self.cms = SHAREPOINT
                raise Exception

        #Meta tag
        if tag == 'meta':
            content = next((b for a,b in attrs if a == 'content'), '')
            name = next((b for a,b in attrs if a == 'name'), '')

            #PHP-Nuke
            if name.lower() == 'generator' and 'PHP-Nuke' in content:
                self.cms = PHPNUKE
                raise Exception

            #EpiServer
            if content.lower() == 'episerver' and name.lower() == 'generator':
                self.cms = EPISERVER
                raise Exception

            #SharePoint
            if content.lower() == 'microsoft sharepoint' and name.lower() == 'generator':
                self.cms = SHAREPOINT
                raise Exception

            #Dynamic web
            if 'dynamicweb' in content.lower() and name.lower() == 'generator':
                self.cms = DYNAMICWEB
                raise Exception


    def handle_comment(self, data):
        for string in self.type3_comment_text:
            if string in data:
                self.cms = TYPO3
                raise Exception


    def handle_endtag(self, tag):
        pass


    def handle_data(self, data):
        if self.parsing_script == True:
            if 'var Drupal = Drupal' in data:
                self.cms = DRUPAL
                raise Exception


def bins():
    return [DOTNETNUKE,
    UMBRACO,
    EPISERVER,
    SHAREPOINT,
    SITECORE,
    DYNAMICWEB,
    WORDPRESS,
    TYPO3,
    PHPNUKE,
    DRUPAL,
    JOOMLA,
    UNKNOWN]

def cms_scanner(website):
    parser = CMSHTMLParser(website)
    try:
        parser.feed(website.html)
    except Exception as e:
        print 'CMSHTMLParser exception: ', e
        print 'site: ', parser.website.url
        if hasattr(e, 'read'):
            print e.read()
    result = parser.cms
    #TODO bin result to bin index
    return ('cms', result)
