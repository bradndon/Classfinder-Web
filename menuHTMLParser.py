from HTMLParser import HTMLParser

class menuHTMLParser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = {}
        self.currentOption = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        if self.NEWTAGS[-1] == "option":
            print data + "\t" + str(self.NEWATTRS[-1])
            self.HTMLDATA[self.currentOption[-2]].append(data.strip())
        if self.NEWTAGS[-1] == "b":
            self.HTMLDATA[data.strip()[:-1]] = []
            self.currentOption.append(data.strip()[:-1])
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
        self.currentOption = []
