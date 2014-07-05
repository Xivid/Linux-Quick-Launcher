from functions import *
import subprocess, webbrowser
#Init & Start-up info
searcher = Searcher()
print "Linux Quick Launcher"
print "Type in keywords to search for apps"
print "Type ':q' to quit program"

while True:
    keyword = raw_input()
    if keyword == "":
        continue
    elif keyword == ":q":
        print "Thanks for using, bye."
        exit()
    else:
        launch_list = searcher.getlist(keyword)

        #console display
        if launch_list == []:
            print "No matching results."
        else: #result ranges from 0 to length-1
             length = len(launch_list)
             for i in range(0, length):
                 print str(i) + ". " + launch_list[i][1]
             choice = eval(raw_input())
             if choice >= 0:
                 print 'will run:' + launch_list[choice][0]
                 subprocess.Popen(launch_list[choice][0])
    #console display


# while True:
#     kw = raw_input()
#     if kw == "":
#         continue
#     if kw == ":q":
#         print "Thanks for using. Bye."
#         exit()
#
#     rekw = kw.replace("*", ".*")
#     rekw = ".*" + rekw.replace("?", ".") + ".*" #replace with regular expressions
#     result = sorted([[namelist[i],  applist[i]] for i in range(len(namelist)) if re.match(rekw.lower(), namelist[i].lower())])
#
#     if result == []:
#         print "No app found!"
#     else: #result ranges from 0 to length-1
#         length = len(result)
#         for i in range(0, length):
#             print str(i) + ". " + result[i][0]
#         choice = eval(raw_input())
#         if choice >= 0:
#             subprocess.Popen(result[choice][1])
