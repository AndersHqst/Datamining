from time import gmtime, strftime
import hmac
import hashlib
import base64
import urllib, urllib2
import json
import os
from lxml import etree

#Keys
ACCESS_KEY = 'AKIAJFMSXA4TJN2S3DCA'
SECRET_ACCESS_KEY = '/ktoB3igoqzssIc6opgiEtf+pIkGSqwtZtUto3CI'

#Simply modify these to execute other queries.
#Examples: http://docs.aws.amazon.com/AlexaWebInfoService/latest/
ACTION_NAME = "UrlInfo";
RESPONSE_GROUP_NAME = "RelatedLinks,Categories,Rank,RankByCountry,RankByCity,UsageStats,ContactInfo,AdultContent,Speed,Language,Keywords,OwnedDomains,LinksInCount,SiteData,LinksInCount";

#service
SERVICE_HOST = "awis.amazonaws.com";
AWS_BASE_URL = "http://" + SERVICE_HOST + "/?";
DATEFORMAT_AWS = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'";
HASH_ALGORITHM = "HmacSHA256";
OUTPUT_DIR = "output/"

def generate_signature(data):
    dig = hmac.new(b'' + SECRET_ACCESS_KEY, msg=data, digestmod=hashlib.sha256).digest()
    return base64.b64encode(dig).decode()

def build_query(time_stamp, action, response_group_name, url):
    """Builds the query. Not all orders are valid."""
    query = "AWSAccessKeyId=" + ACCESS_KEY
    query += "&Action=" + action
    query += "&ResponseGroup=" + urllib.quote(response_group_name)
    query += "&SignatureMethod=" + HASH_ALGORITHM
    query += "&SignatureVersion=" + "2"
    query += "&Timestamp=" + urllib.quote(time_stamp)
    query += "&Url=" + url
    return query

def execute(site, action=ACTION_NAME, response_group_name=RESPONSE_GROUP_NAME):
    #Not completely correct time stamp, last zero in miliseconds is just inserted, not sure how to get it
    time_stamp = strftime("%Y-%m-%dT%H:%M:%S.123Z", gmtime())
    query = build_query(time_stamp, action, response_group_name, site)
    sign = "GET\n" + SERVICE_HOST + "\n/\n" + query;
    signature = generate_signature(sign)
    uri = AWS_BASE_URL + query + "&" + urllib.urlencode({"Signature": signature});

    #Send request
    resp = urllib2.urlopen(uri)

    lines = resp.readlines()
    xml = ''.join(lines)
    return xml

def get_xml_value_or_default(element, default):
    if element is None or element.text is None:
        value = default
    else:
        value = element.text
    return value

def get_alexa_data(url):
    # Fix URL format
    url = url.replace('http://', '')

    # Remove stupid namespaces
    xml = execute(url).replace('aws:','')
    root = etree.fromstring(xml)

    content_data = root.find('.//ContentData')
    traffic_data = root.find('.//TrafficData')

    title_elem = content_data.find('SiteData/Title')
    title = get_xml_value_or_default(title_elem, '')

    description_elem = content_data.find('SiteData/Description')
    description = get_xml_value_or_default(description_elem, '')

    load_time_elem = content_data.find('Speed/MedianLoadTime')
    load_time = int(get_xml_value_or_default(load_time_elem, -1))

    has_adult_content_elem = content_data.find('AdultContent')
    has_adult_content = get_xml_value_or_default(has_adult_content_elem, 'no') == 'yes'

    langauge_elem = content_data.find('Language/Locale')
    langauge = get_xml_value_or_default(langauge_elem, '')

    links_in_elem = content_data.find('LinksInCount')
    links_in = int(get_xml_value_or_default(links_in_elem, -1))

    total_rank_elem = traffic_data.find('Rank')
    total_rank = int(get_xml_value_or_default(total_rank_elem, -1))

    dk_rank_elem = traffic_data.find("RankByCountry/Country[@Code='DK']/Rank")
    dk_rank = int(get_xml_value_or_default(dk_rank_elem, -1))

    return {
        'title': title,
        'description': description,
        'load_time': load_time,
        'has_adult_content': has_adult_content,
        'langauge': langauge,
        'links_in': links_in,
        'total_rank': total_rank,
        'dk_rank': dk_rank
    }