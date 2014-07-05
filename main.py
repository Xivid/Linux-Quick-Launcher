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
                 print str(i) + ". " + launch_list[i]['Name']
                 print '  ' + launch_list[i]['Comment']
             choice = eval(raw_input())
             if choice >= 0:
                 print 'will execute:' + launch_list[choice]['Exec']
                 subprocess.Popen(launch_list[choice]['Exec'])
    #console display

