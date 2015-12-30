import urllib2
import json
from menuHTMLParser import menuHTMLParser

def getHTTP():
    url = 'https://admin.wwu.edu/pls/wwis/wwsktime.SelClass'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()

def extractSubjects(http):
    parser = menuHTMLParser()
    parser.feed(http)

    # Extract data from parser
    tags  = parser.NEWTAGS
    attrs = parser.NEWATTRS
    data  = parser.HTMLDATA

    # Clean the parser
    parser.clean()



    
    for key, value in data.iteritems():
        messed = []
        for index, s in enumerate(data[key]):
            if " - " not in s and (key == "Subject" or key == "GUR/Course Attribute"):
                messed.append(index)
            elif not s:
                messed.append(index)
            elif "All" in s:
                print s
        for n in reversed(messed[1:]):
            data[key][n-1] += " " + data[key][n]
            del data[key][n]
    data = dict((k, v) for k, v in data.iteritems() if v)
    for key in data:
        data[key] = filter(None, data[key])
        map(str.strip, data[key])
    #Print out our data
    # for option in data:
    #     print option
    #     for s in data[option]:
    #
    #         print "\t" + s
    print json.dumps(data)


if __name__ == "__main__":
    extractSubjects(getHTTP())
