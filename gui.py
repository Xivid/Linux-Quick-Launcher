from Tkinter import *
import os
import re
import subprocess

def init():
    global namelist, applist
    namelist = sorted([app for app in os.listdir("/usr/share/applications") if app[-8:] == ".desktop"])
    applist = [app[:-8] for app in namelist]
    getname(namelist)

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

def run(app):
    subprocess.Popen(app,  shell = True)
    
def search(event):
    global namelist, applist, result, apps, width, height
    kw = entry.get()
    try:
        apps.delete(0, apps.size())
        apps.destroy()
    except:
        pass
    if kw == ":quit":
        root.destroy()

    rekw = kw.replace("*", ".*")
    rekw = ".*" + rekw.replace("?", ".") + ".*"
    result = sorted([[namelist[i],  applist[i]] for i in range(len(namelist)) if re.match(rekw.lower(), namelist[i].lower())])
    sum = len(result)

    if kw != "" and sum != 0:            
        
        if sum < 20:
            root.geometry("{}x{}+0+0".format(width, 35 + height * sum + int(12.21 - sum * 2.21)))
            apps = Listbox(root, width = 25, height = sum, font = " -25")           
        else:
            root.geometry("{}x{}+0+0".format(width, 35 + height * 20 - 28))
            apps = Listbox(root, width = 25, height = 20, font = " -25")  
        
        apps.place(x = 5, y = 10 + height)
        for i in range(sum):
            apps.insert(i, result[i][0])
    else:
        root.geometry("{}x{}+0+0".format(width, 35))
        
namelist, applist, result, apps = [], [], [], []
width, height = 240, 25
root = Tk()

root.maxsize(width, 10 + height * 21)
root.minsize(240, 10 + height)
root.geometry("{}x{}+0+0".format(width, 35))

root.title("Linux Quick Launcher")

entry = Entry(root, width = 32)
entry.place(x = 5, y = 5)
entry.bind("<KeyRelease>", search)

init()
root.mainloop()
