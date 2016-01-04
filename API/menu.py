import urllib2
import json
from classFinderHTMLParsers import menuHTMLParser

def getHTTP():
    url = 'https://admin.wwu.edu/pls/wwis/wwsktime.SelClass'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()

def extractData(http):
    parser = menuHTMLParser()
    parser.feed(http)

    data  = parser.HTMLDATA

    # Clean the parser
    parser.clean()
    data = dict((k, v) for k, v in data.iteritems() if v)

    return json.dumps(data)


if __name__ == "__main__":
    extractData(getHTTP())
