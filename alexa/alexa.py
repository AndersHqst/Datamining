from time import gmtime, strftime
import hmac
import hashlib
import base64
import urllib, urllib2
import json
import os

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

def build_query2(time_stamp, action, response_group_name, url):
    return urllib.urlencode(
    {
        "AWSAccessKeyId": ACCESS_KEY,
        "Action": action,
        "ResponseGroup": response_group_name,
        "SignatureMethod": HASH_ALGORITHM,
        "SignatureVersion": "2",
        "Timestamp": time_stamp,
        "Url": url
    })

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
    print 'uri: ' + uri

    # uri = 'http://awis.amazonaws.com/?AWSAccessKeyId=AKIAJFMSXA4TJN2S3DCA&Action=UrlInfo&ResponseGroup=Rank%2CContactInfo%2CLinksInCount&SignatureMethod=HmacSHA256&SignatureVersion=2&Timestamp=2013-04-17T16%3A29%3A14.429Z&Url=www.dr.dk&Signature=5jj4eLkbXa4C7lIEcKp%2BL7DbZVLorNossyEhFFwWMJc%3D'
    #Send request
    try:
        resp = urllib2.urlopen(uri)
    except Exception, e:
        print "Couldn't do it: %s" % e
    lines = resp.readlines()

    #Find or create outout dir
    directory = "./output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    #Write result to data file
    data_file = open(directory + '/data_' + time_stamp + '.xml', 'w')
    data_file.write(''.join(lines))
    data_file.close()

    #Write result to log file
    log_file = open(directory + '/log_' + time_stamp + '.json', 'w')
    log = json.dumps({"query": query, "sign": sign, "signature": signature, "uri": uri},
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': '))
    log_file.write(log)
    log_file.close()

# execute('www.webcoders.dk')
