import os
import re
import subprocess

def getname(l):
    i = 0
    for app in l:
        fp = open("/usr/share/applications/" + app,  "r")
        name = "init"
        flag = False
        
        while name:
            name = fp.readline()
            if name[:4] == "Name":
                flag = True
                break
                
        name = name[name.find("=") + 1:-1] if flag else ""
        l[i] = name
        
        fp.close()
        i += 1

namelist = sorted([app for app in os.listdir("/usr/share/applications") if app[-8:] == ".desktop"])
applist = [app[:-8] for app in namelist]
getname(namelist)

print "Linux Quick Launcher"
print "Type keyword to find or search app"
print "Type 'exit' to exit program"


while True:
    kw = raw_input()
    if kw == "":
        continue
    if kw.lower() == "exit":
        exit()
    
    rekw = kw.replace("*", ".*")
    rekw = ".*" + rekw.replace("?", ".") + ".*"
    result = sorted([[namelist[i],  applist[i]] for i in range(len(namelist)) if re.match(rekw.lower(), namelist[i].lower())])
    
    if result == []:
        print "No app found!"
    elif len(result) == 1 and kw.lower() == result[0][0].lower():
        subprocess.Popen(result[0][1],  shell = True)
    else:
        i = 1
        for app in result:
            print str(i) + ". " + app[0]
            i += 1
