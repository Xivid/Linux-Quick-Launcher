import os
import re

class Searcher:
    def __init__(self):
        #namelist: .desktop filename (initially) -> Name property
        self.namelist = sorted([app for app in os.listdir("/usr/share/applications") if app[-8:] == ".desktop"])
        self.launchlist = [app[:-8] for app in self.namelist] #applist: launch name
        self.length = len(self.namelist)
        for i in range(self.length):
            fp = open("/usr/share/applications/" + self.namelist[i], "r")

            name = fp.readline()
            while name[:4] != 'Name': # ".desktop" file must have a Name property
                name = fp.readline()

            self.namelist[i] = name.split('=')[1].strip()

            fp.close()

    def getlist(self, keyword):
        '''
            ret[i][0]: launch name
            ret[i][1]: Name property
        '''
        rekw = ".*" + keyword.replace("*", ".*").replace("?", ".") + ".*" #replace with regular expressions
        result = sorted([[self.launchlist[i], self.namelist[i]] for i in range(self.length) if re.match(rekw.lower(), self.namelist[i].lower())])

        return result