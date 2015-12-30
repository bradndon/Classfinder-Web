from HTMLParser import HTMLParser

import urllib
import urllib2

url = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass' # write the url here
subjects = {"Spanish" : "SPAN", "Computer Science" : "CSCI", "Art History" : "A/HI", "Accounting" : "ACCT"}
values = {'sel_subj' : ['dummy', 'dummy', 'A/HI', 'ACCT','CSCI','SPAN'],
        'sel_inst' : 'ANY',
        'sel_gur' : ['dummy', 'dummy', 'All'],
        'sel_day' : 'dummy',
        'sel_open' : ['dummy', ''],
        'sel_crse' : '',
        'begin_hh': '00',
        'begin_mi': 'A',
        'end_hh': '00',
        'end_mi': 'A',
        'sel_cdts': 'All',
        'term': '201610'}


data = urllib.urlencode(values, doseq=True)
print data
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()


class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []

parser = myhtmlparser()
parser.feed(the_page)

# Extract data from parser
tags  = parser.NEWTAGS
attrs = parser.NEWATTRS
data  = parser.HTMLDATA

# Clean the parser
parser.clean()

#Print out our data
#print tags
# print attrs
currClass = []
crns = []
allClasses = []
classNames = []


for attr in attrs:
    if ('type', 'submit') in attr:
        crns.append(attr[2][1])
currSubj = ""
add = False
currClass.append(data[0])
for s in data:
    currData = s.strip()
    if currData:
        parts = currData.split(" ")
        if currClass and currSubj == parts[0] and len(parts) == 2:
            index = 0
            while index != len(currClass) - 1  and currSubj not in currClass[index]:
                index += 1
            currParts = currClass[index].split(" ")
            try:
                if int(currParts[1][0:3]) <= int(parts[1][0:3]):
                    lastClass = currClass
                    if "CLOSED" in currClass[1:] or "CLOSED:   Waitlist Available" in currClass[1:]:
                        currClass = lastClass[-1:]
                        del lastClass[-1]
                    else:
                        currClass = []
                    allClasses.append(lastClass)
                    currClass.append(currData)
                    classNames.append( currData)
            except:
                currClass.append(currData)
                print "FAILED"
                continue

        if currClass:
            currClass.append(currData)
        if not add and currData == "Addl Chrgs":
            if len(currClass) > 0:
                currSubj =  subjects[currClass[-14]]
                allClasses.append(currClass[0:-14])
                currClass = []
            add = True
        elif add:
            classNames.append(currData)
            currClass.append(currData)
            add = False
allClasses.append(currClass)
print len(crns)
print len(classNames)
for index, c in enumerate(allClasses):
    if c:
        c.append(crns[index])
        #print c
    else:
        print "EMPTY################################"
