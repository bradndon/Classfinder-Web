from HTMLParser import HTMLParser

import urllib
import urllib2
import json
import sys
from classFinderHTMLParsers import classesHTMLParser

def test(subject, verbose=False):
    if subject != "All":
        number = getNumClasses(subject)
        classes = getClasses(subject, verbose)

        print subject + "\t" + str(number == classes)
        assert classes == number, subject + " is not the correct amount of classes\nCorrect number: " + str(number) + "\nYour number: " + str(classes)

def getClasses(subject, verbose=False):
    url = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass' # write the url here
    subjects = {
    	"International Business": "IBUS",
    	"Engineering Technology": "ETEC",
    	"Canadian/American Studies": "C/AM",
    	"Info Systms Security": "CISS",
    	"Modern and Classical Language": "LANG",
    	"Decision Sciences": "DSCI",
    	"Philosophy": "PHIL",
    	"American Cultural Studies": "AMST",
    	"French": "FREN",
    	"Entrepreneurship": "ENTR",
    	"Anthropology": "ANTH",
    	"Computer Science": "CSCI",
    	"Communication Sci & Disorders": "CSD",
    	"Kinesiology": "KIN",
    	"Rehabilitation Counseling": "RC",
    	"Italian": "ITAL",
    	"Art": "ART",
    	"Nursing": "NURS",
    	"Early Childhood Education": "ECE",
    	"Adult and Higher Ed": "AHE",
    	"Electrical Engineering": "EE",
    	"Education": "EDUC",
    	"Sexuality Stdy": "WGSS",
    	"Materials Science": "MSCI",
    	"Management": "MGMT",
    	"Industrial Design": "ID",
    	"Manufacturing Engineering": "MFGE",
    	"Secondary Education": "SEC",
    	"Environmental Sciences": "ESCI",
    	"Eurasian Studies": "EUS",
    	"Health Education": "HLED",
    	"Biology": "BIOL",
    	"Latin": "LAT",
    	"Compass to Campus": "C2C",
    	"Astronomy": "ASTR",
    	"Elementary Education": "ELED",
    	"Liberal Studies": "LBRL",
    	"Fairhaven": "FAIR",
    	"Economics": "ECON",
    	"English Language Learners": "ELL",
    	"Instructional Technology": "I T",
    	"Greek": "GREK",
    	"Student Affairs Administration": "SAA",
    	"English": "ENG",
    	"Physical Education": "PE",
    	"Chemistry": "CHEM",
    	"Chinese": "CHIN",
    	"Dance": "DNC",
    	"Energy": "ENRG",
    	"&": "WGSS",
    	"Industrial Tech-Vehicle Design": "VHCL",
    	"Design": "DSGN",
    	"Arabic": "ARAB",
    	"Leadership Studies": "LDST",
    	"Honors": "HNRS",
    	"Linguistics": "LING",
    	"Psychology": "PSY",
    	"Disorders": "CSD",
    	"Music": "MUS",
    	"Women, Gender & Sexuality Stdy ": "WGSS",
    	"Political Science": "PLSC",
    	"Korean": "KORE",
    	"Theatre Arts": "THTR",
    	"East Asian Studies": "EAST",
    	"Finance": "FIN",
    	"Geology": "GEOL",
    	"Science Education": "SCED",
    	"Russian": "RUSS",
    	"Operations Management": "OPS",
    	"History": "HIST",
    	"Art History": "A/HI",
    	"Plastics Engineering": "PCE",
    	"German": "GERM",
    	"Teaching Eng/Second Language": "TESL",
    	"Educational Administration": "EDAD",
    	"All Subjects ": "All",
    	"Library": "LIBR",
    	"Mathematics/Computer Science": "M/CS",
    	"Engineering": "PCE",
    	"Seminar": "SMNR",
    	"Sociology": "SOC",
    	"Management Information Systems": "MIS",
    	"Mathematics": "MATH",
    	"Marketing": "MKTG",
    	"Communication Studies": "COMM",
    	"Environmental Studies": "ENVS",
    	"Continuing & College Education": "CCE",
    	"Coaching Development": "CD",
    	"Recreation": "RECR",
    	"Master of Professional ACCT": "MPAC",
    	"Human Resource Management": "HRM",
    	"Journalism": "JOUR",
    	"Classical Studies": "CLST",
    	"Human Services": "HSP",
    	"Master of Business Admin": "MBA",
    	"Physics": "PHYS",
    	"Portuguese": "PORT",
    	"Special Education": "SPED",
    	"College Education": "CCE",
    	"Japanese": "JAPN",
    	"Computr & Info Systms Security": "CISS",
    	"Spanish": "SPAN",
    	"Accounting": "ACCT",
    	"International Studies": "INTL",
    	"Multidisciplinary Studies": "MDS",
    	"Geography": "EGEO"
    }
    values = {'sel_subj' : ['dummy', 'dummy', subject, subject],
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
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    parser = classesHTMLParser()
    parser.feed(the_page)
    tags  = parser.NEWTAGS
    attrs = parser.NEWATTRS
    data  = parser.HTMLDATA

    # Clean the parser
    parser.clean()
    count = 0
    if verbose:
        for index, d in enumerate(data):
            for s in d:
                print s
            print "--------------------------------------"
    return len(data)
    # class myhtmlparser(HTMLParser):
    #     def __init__(self):
    #         self.reset()
    #         self.NEWTAGS = []
    #         self.NEWATTRS = []
    #         self.HTMLDATA = []
    #     def handle_starttag(self, tag, attrs):
    #         self.NEWTAGS.append(tag)
    #         self.NEWATTRS.append(attrs)
    #     def handle_data(self, data):
    #         self.HTMLDATA.append(data)
    #     def clean(self):
    #         self.NEWTAGS = []
    #         self.NEWATTRS = []
    #         self.HTMLDATA = []
    #
    # parser = myhtmlparser()
    # parser.feed(the_page)
    #
    # # Extract data from parser
    # tags  = parser.NEWTAGS
    # attrs = parser.NEWATTRS
    # data  = parser.HTMLDATA
    #
    # # Clean the parser
    # parser.clean()
    #
    # #Print out our data
    # #print tags
    # # print attrs
    # currClass = []
    # crns = []
    # allClasses = []
    # classNames = []
    #
    #
    # for attr in attrs:
    #     if ('type', 'submit') in attr:
    #         crns.append(attr[2][1])
    # currSubj = ""
    # add = False
    # currClass.append(data[0])
    # for s in data:
    #     currData = s.strip()
    #     if currData:
    #         parts = currData.split(" ")
    #         if currClass and currSubj == parts[0] and len(parts) == 2:
    #             index = 0
    #             while index != len(currClass) - 1  and currSubj not in currClass[index]:
    #                 index += 1
    #             currParts = currClass[index].split(" ")
    #             try:
    #                 if int(currParts[1][0:3]) <= int(parts[1][0:3]) and "co-requisit" not in currClass[-1]:
    #                     lastClass = currClass
    #                     if "CLOSED" in currClass[1:] or "CLOSED:   Waitlist Available" in currClass[1:]:
    #                         currClass = lastClass[-1:]
    #                         del lastClass[-1]
    #                     else:
    #                         currClass = []
    #                     allClasses.append(lastClass)
    #                     currClass.append(currData)
    #                     classNames.append( currData)
    #             except:
    #                 currClass.append(currData)
    #                 # print "FAILED"
    #                 continue
    #
    #         if currClass:
    #             currClass.append(currData)
    #         if not add and currData == "Addl Chrgs":
    #             if len(currClass) > 0:
    #                 currSubj =  subjects[currClass[-14]]
    #                 allClasses.append(currClass[0:-14])
    #                 currClass = []
    #             add = True
    #         elif add:
    #             classNames.append(currData)
    #             currClass.append(currData)
    #             add = False
    # allClasses.append(currClass)
    # if verbose:
    #     print len(crns)
    #     print len(classNames)
    # del allClasses[0]
    # for index, c in enumerate(allClasses):
    #     if c:
    #         if verbose:
    #             print c
    #     # else:
    #     #     print "EMPTY################################"
    # return len(classNames)
    #
    # return json.dumps(allClasses)


def getNumClasses(subject):
    url = 'https://admin.wwu.edu/pls/wwis/wwsktime.ListClass' # write the url here
    values = {'sel_subj' : ['dummy', 'dummy', subject, subject],
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
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()
    class myhtmlparser(HTMLParser):
        def __init__(self):
            self.reset()
            self.NEWATTRS = []
        def handle_starttag(self, tag, attrs):
            self.NEWATTRS.append(attrs)
        def clean(self):
            self.NEWATTRS = []

    parser = myhtmlparser()
    parser.feed(the_page)

    # Extract data from parser
    attrs = parser.NEWATTRS

    # Clean the parser
    parser.clean()


    crns = []


    for attr in attrs:
        if ('type', 'submit') in attr:
            crns.append(attr[2][1])
    return len(crns)

if __name__ == "__main__":
    subjects = {
    	"International Business": "IBUS",
    	"Engineering Technology": "ETEC",
    	"Canadian/American Studies": "C/AM",
    	"Info Systms Security": "CISS",
    	"Modern and Classical Language": "LANG",
    	"Decision Sciences": "DSCI",
    	"Philosophy": "PHIL",
    	"American Cultural Studies": "AMST",
    	"French": "FREN",
    	"Entrepreneurship": "ENTR",
    	"Anthropology": "ANTH",
    	"Computer Science": "CSCI",
    	"Communication Sci & Disorders": "CSD",
    	"Kinesiology": "KIN",
    	"Rehabilitation Counseling": "RC",
    	"Italian": "ITAL",
    	"Art": "ART",
    	"Nursing": "NURS",
    	"Early Childhood Education": "ECE",
    	"Adult and Higher Ed": "AHE",
    	"Electrical Engineering": "EE",
    	"Education": "EDUC",
    	"Sexuality Stdy": "WGSS",
    	"Materials Science": "MSCI",
    	"Management": "MGMT",
    	"Industrial Design": "ID",
    	"Manufacturing Engineering": "MFGE",
    	"Secondary Education": "SEC",
    	"Environmental Sciences": "ESCI",
    	"Eurasian Studies": "EUS",
    	"Health Education": "HLED",
    	"Biology": "BIOL",
    	"Latin": "LAT",
    	"Compass to Campus": "C2C",
    	"Astronomy": "ASTR",
    	"Elementary Education": "ELED",
    	"Liberal Studies": "LBRL",
    	"Fairhaven": "FAIR",
    	"Economics": "ECON",
    	"English Language Learners": "ELL",
    	"Instructional Technology": "I T",
    	"Greek": "GREK",
    	"Student Affairs Administration": "SAA",
    	"English": "ENG",
    	"Physical Education": "PE",
    	"Chemistry": "CHEM",
    	"Chinese": "CHIN",
    	"Dance": "DNC",
    	"Energy": "ENRG",
    	"&": "WGSS",
    	"Industrial Tech-Vehicle Design": "VHCL",
    	"Design": "DSGN",
    	"Arabic": "ARAB",
    	"Leadership Studies": "LDST",
    	"Honors": "HNRS",
    	"Linguistics": "LING",
    	"Psychology": "PSY",
    	"Disorders": "CSD",
    	"Music": "MUS",
    	"Women, Gender & Sexuality Stdy ": "WGSS",
    	"Political Science": "PLSC",
    	"Korean": "KORE",
    	"Theatre Arts": "THTR",
    	"East Asian Studies": "EAST",
    	"Finance": "FIN",
    	"Geology": "GEOL",
    	"Science Education": "SCED",
    	"Russian": "RUSS",
    	"Operations Management": "OPS",
    	"History": "HIST",
    	"Art History": "A/HI",
    	"Plastics Engineering": "PCE",
    	"German": "GERM",
    	"Teaching Eng/Second Language": "TESL",
    	"Educational Administration": "EDAD",
    	"All Subjects ": "All",
    	"Library": "LIBR",
    	"Mathematics/Computer Science": "M/CS",
    	"Engineering": "PCE",
    	"Seminar": "SMNR",
    	"Sociology": "SOC",
    	"Management Information Systems": "MIS",
    	"Mathematics": "MATH",
    	"Marketing": "MKTG",
    	"Communication Studies": "COMM",
    	"Environmental Studies": "ENVS",
    	"Continuing & College Education": "CCE",
    	"Coaching Development": "CD",
    	"Recreation": "RECR",
    	"Master of Professional ACCT": "MPAC",
    	"Human Resource Management": "HRM",
    	"Journalism": "JOUR",
    	"Classical Studies": "CLST",
    	"Human Services": "HSP",
    	"Master of Business Admin": "MBA",
    	"Physics": "PHYS",
    	"Portuguese": "PORT",
    	"Special Education": "SPED",
    	"College Education": "CCE",
    	"Japanese": "JAPN",
    	"Computr & Info Systms Security": "CISS",
    	"Spanish": "SPAN",
    	"Accounting": "ACCT",
    	"International Studies": "INTL",
    	"Multidisciplinary Studies": "MDS",
    	"Geography": "EGEO"
    }
    verbose = False
    args = sys.argv
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")
    print args
    if len(args) >= 2:
        test(args[1], verbose)
    else:
        for k,v in subjects.iteritems():
            test(v, verbose)
