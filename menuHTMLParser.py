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
