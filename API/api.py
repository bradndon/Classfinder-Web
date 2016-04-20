#!/usr/bin/env python

#Copyright (C) Brandon Fox 2016

from HTMLParser import HTMLParser

import urllib
import urllib2
import json
import sys
import random
import string
from classFinderHTMLParsers import classesHTMLParser

def id_generator(size=36, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def test(subject, verbose=False):
    number = getNumClasses(subject)
    classes = getClasses(subject, 201620, verbose, True)

    print subject + "\t" + str(number == classes)
    assert classes == number, subject + " is not the correct amount of classes\nCorrect number: " + str(number) + "\nYour number: " + str(classes)

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def getClasses(subject, term, verbose=False, test=False):
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
            'term': term}

    parts = ["addl", "restrictions", "prerequisites", "other", "time2", "room2"]
    data = urllib.urlencode(values, doseq=True)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    parser = classesHTMLParser()
    parser.feed(the_page)
    tags  = parser.NEWTAGS
    attrs = parser.NEWATTRS
    data  = parser.HTMLDATA
    classattr = parser.CLASSATTRS
    crn = parser.crn
    # Clean the parser
    parser.clean()

    crns = []
    for attr in attrs:
        if ('type', 'submit') in attr:
            crns.append(attr[2][1])
    count = 0
    if verbose:
        for k, v in data.iteritems():
            for index, d in enumerate(v):
                for ind, s in enumerate(d):
                    print s + "\t\t\t" +  str(classattr[k][index][ind])
                print "--------------------------------------"
    allReturns = {}
    returns = []
    totalIndex = 0
    for k,v in sorted(data.iteritems()):
        for index, aClass in enumerate(v):
            rest = False
            prereq = False
            other = False
            added = False
            returns.append({})
            if "CLOSED" in aClass[0]:
                returns[-1]["open"] = "false"
                del aClass[0]
                del classattr[k][index][0]
            else:
                returns[-1]["open"] = "true"
            returns[-1]["class"] = aClass[0]
            returns[-1]["courseNum"] = aClass[0].split(" ")[-1]
            counter =  2
            returns[-1]["title"] = aClass[1]
            while not RepresentsInt(aClass[counter]):
                returns[-1]["title"] +=  " " + aClass[counter]
                counter += 1
            returns[-1]["cap"] = int(aClass[counter])
            returns[-1]["enrol"] = int(aClass[counter + 1])
            returns[-1]["avail"] = int(aClass[counter + 2])
            temp = aClass[counter+3].split(" ")
            instr = ""
            if len(temp) > 1:
                for i, s in enumerate(temp):
                    instr +=  s + " "
                    if "," in s:
                        instr += temp[i+1]
                        break;
            else:
                instr = aClass[counter+3]
            returns[-1]["inst"] = instr
            returns[-1]["dates"] = aClass[counter + 4]
            if ('color', 'black') in classattr[k][index][counter + 5]:
                returns[-1]["gur"] = aClass[counter + 5]
                counter += 1
            else:
                returns[-1]["gur"] = None
            returns[-1]["time1"] = aClass[counter + 5]
            beginTime = 0
            endTime = 0
            for word in aClass[counter + 5].split(" "):
                if "-" in word:
                    times = word.split("-")
                    beginTime = ''.join(times[0].split(":"))
                    endTime = ''.join(times[1].split(":"))
                    try:
                        beginTime = int(beginTime)
                        endTime = int(endTime)
                        if "pm" in aClass[counter + 5].split(" ")[-1] and endTime < 1200:

                            if beginTime <= endTime:
                                beginTime += 1200
                            endTime += 1200
                        returns[-1]["beginTime"] = beginTime
                        returns[-1]["endTime"] = endTime
                    except:
                        continue
            returns[-1]["daytime"] = []
            days = aClass[counter + 5].split(" ")[0]
            if days != "TBA":
                for day in list(days):
                    returns[-1]["daytime"].append([day,beginTime,endTime])

            returns[-1]["room1"] = aClass[counter + 6]
            returns[-1]["crenum"] = aClass[counter + 7]
            length = len(aClass)
            while length -1 > counter + 8:
                added = False
                if aClass[counter + 8][0] == "$":
                    returns[-1]["addl"] = aClass[counter + 8]
                    added = True
                if "Restrictions:" == aClass[counter + 8]:
                    rest = True
                    added = True
                    counter += 1
                    returns[-1]["restrictions"] = aClass[counter + 8]
                if "Prerequisites:" == aClass[counter + 8]:
                    prereq = True
                    rest = False
                    added = True
                    counter += 1
                    returns[-1]["prerequisites"] = aClass[counter + 8]
                if not other and ([('size', '-2')] == classattr[k][index][counter + 8] or [('size', '-1')] == classattr[k][index][counter + 8]):
                    prereq = False
                    rest = False
                    other = True
                    added = True
                    returns[-1]["other"] = aClass[counter + 8]
                if not added:
                    if rest:
                        returns[-1]["restrictions"] += " " + aClass[counter + 8]
                    elif prereq:
                        returns[-1]["prerequisites"] += " " + aClass[counter + 8]
                    elif other:
                        returns[-1]["other"] += " " + aClass[counter + 8]
                    else:
                        returns[-1]["time2"] = aClass[counter + 8]
                        for word in aClass[counter + 8].split(" "):
                            if "-" in word:
                                times = word.split("-")
                                beginTime = ''.join(times[0].split(":"))
                                endTime = ''.join(times[1].split(":"))
                                try:
                                    beginTime = int(beginTime)
                                    endTime = int(endTime)
                                    if "pm" in aClass[counter + 8].split(" ")[-1] and endTime < 1200:
                                        if beginTime <= endTime:
                                            beginTime += 1200
                                        endTime += 1200
                                    if "beginTime" in returns[-1]:
                                        if beginTime < returns[-1]["beginTime"]:
                                            returns[-1]["beginTime"] = beginTime
                                    else:
                                        returns[-1]["beginTime"] = beginTime
                                    if "endTime" in returns[-1]:
                                        if endTime > returns[-1]["endTime"]:
                                            returns[-1]["endTime"] = endTime
                                    else:
                                        returns[-1]["endTime"] = endTime

                                except:
                                    continue
                        days = aClass[counter + 8].split(" ")[0]
                        if days != "TBA":
                            for day in list(days):
                                returns[-1]["daytime"].append([day,beginTime,endTime])
                        counter += 1
                        returns[-1]["room2"] = aClass[counter + 8]

                counter += 1
            returns[-1]["crn"] = aClass[len(aClass) - 1]
            totalIndex += 1
            for part in parts:
                if part not in returns[-1]:
                    returns[-1][part] = None
        allReturns[k] = returns
        returns = []
    allReturns[k][-1]["crn"] = crn
    if verbose:
        print json.dumps(allReturns)
    if test:
        for k,v in data.iteritems():
            if subjects[k] == subject:
                return len(data[k])
    else:
        return json.dumps(allReturns)



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
            'term': '201620'}
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
    from shutil import copyfile
    f = open('./temp.json','w')
    f.write(getClasses("All", 201640, False, False))
    f.close()
    copyfile('./temp.json', '/var/www/html/classes.json')
    f = open('./temp.json','w')
    f.write(getClasses("All", 201630, False, False))
    f.close()
    copyfile('./temp.json', '/var/www/html/classes2.json')
    f = open('./temp.json','w')
    f.write(getClasses("All", 201620, False, False))
    f.close()
    copyfile('./temp.json', '/var/www/html/classes3.json')
