#Copyright (C) Brandon Fox 2016

from HTMLParser import HTMLParser

class menuHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = {}
        self.currentOption = []
        self.lastData = ""
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        if self.NEWTAGS[-1] == "option":
            #print data + "\t" + str(self.NEWATTRS[-1])
            if " - " in data.strip():
                data = data.strip().split(' - ')[-1]
            if self.NEWATTRS[-1][-1][1] in self.HTMLDATA[self.currentOption[-2]].values():
                self.HTMLDATA[self.currentOption[-2]][self.lastData + " " + data.strip()] = self.NEWATTRS[-1][-1][1]
                self.HTMLDATA[self.currentOption[-2]][data.strip()] = self.NEWATTRS[-1][-1][1]

                del self.HTMLDATA[self.currentOption[-2]][self.lastData]
                self.lastData = self.lastData + " " + data.strip()
            else:
                self.HTMLDATA[self.currentOption[-2]][data.strip()] = self.NEWATTRS[-1][-1][1]
                self.lastData = data.strip()
        if self.NEWTAGS[-1] == "b":
            self.HTMLDATA[data.strip()[:-1]] = {}
            self.currentOption.append(data.strip()[:-1])
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
        self.currentOption = []

class classesHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = {}
        self.ALL = []
        self.CLASSATTRS = {}
        self.lastData = ""
        self.currSubj = ""
        self.crn = 0
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
        # if ('type', 'submit') in attrs:
        #     continue
            # print self.NEWATTRS[-1][2][1]
            # print self.CLASSATTRS
            # self.CLASSATTRS[self.currSubj][-1].append(self.NEWATTRS[-1][2][1])
    def handle_data(self, data):
        if ('type', 'submit') in self.NEWATTRS[-1]:
            self.crn = self.NEWATTRS[-1][2][1]
        if self.NEWTAGS[-1] == "a" and data.strip() and "table" in self.NEWTAGS:
            if self.HTMLDATA and "Addl Chrgs" in self.HTMLDATA[self.currSubj][-1]:
                pastSub = self.currSubj
                index = self.HTMLDATA[pastSub][-1].index("Class")
                self.currSubj = self.HTMLDATA[pastSub][-1][index-1]
                self.HTMLDATA[self.currSubj] = []
                self.CLASSATTRS[self.currSubj] = []
                self.HTMLDATA[pastSub][-1] = self.HTMLDATA[pastSub][-1][:index-1]
                self.HTMLDATA[pastSub][-1].append(self.crn)
                self.crn = 0
            elif not self.HTMLDATA:
                self.currSubj = self.ALL[self.ALL.index("Class") - 1]
                self.HTMLDATA[self.currSubj] = []
                self.CLASSATTRS[self.currSubj] = []
            if self.crn > 0:
                self.HTMLDATA[self.currSubj][-1].append(self.crn)
            self.HTMLDATA[self.currSubj].append([])
            self.CLASSATTRS[self.currSubj].append([])
            if "CLOSED" in self.lastData:
                self.HTMLDATA[self.currSubj][-1].append(self.lastData)
                self.CLASSATTRS[self.currSubj][-1].append(())
                if len(self.HTMLDATA[self.currSubj]) > 1:
                    self.HTMLDATA[self.currSubj][-2].pop(-2)
            self.HTMLDATA[self.currSubj][-1].append(data.strip())
            self.CLASSATTRS[self.currSubj][-1].append(self.NEWATTRS[-1])
        elif data.strip() and len(self.HTMLDATA) > 0:
            self.HTMLDATA[self.currSubj][-1].append(data.strip())
            self.CLASSATTRS[self.currSubj][-1].append(self.NEWATTRS[-1])

        if data.strip():
            self.ALL.append(data.strip())
            self.lastData = data.strip()
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
