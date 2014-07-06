import os
import re
import locale

class Executable:
    def __init__(self, desktop = None):
        self.Name = ""
        self.Type = "" # we only process those with Type "Application"
        self.Comment = "" #GenericName or Comment
        self.Exec = ""
        self.Keywords = "" #split by ';', composed by Name(+locale);Comment(+locale);GenericName(+locale);Categories;
        if desktop is not None:
            #Interpret the file
            dic = dict()
            f = open(desktop, "r")
            line = f.readline()
            while line:
                if line.find('=') > -1:
                    line = line.strip().split('=', 1)
                    dic[line[0]] = line[1]

                elif line[:8]=='[Desktop' and line[9:15]!='Entry]':
                    break
                line = f.readline()
            f.close()

            self.Name = dic['Name'] if 'Name' in dic else ''
            self.Type = dic['Type'] if 'Type' in dic else ''
            self.Comment = dic['Comment'] if 'Comment' in dic else (dic['GenericName'] if 'GenericName' in dic else '')
            self.Exec = dic['Exec'].replace(" %u", "").replace(" %U", "") if 'Exec' in dic else ''
            self.Keywords = ((dic['Name']+';') if 'Name' in dic else '')+\
                            ((dic['Name'+'['+locale.getdefaultlocale()[0]+']'] + ';') if 'Name'+'['+locale.getdefaultlocale()[0]+']' in dic else '')+\
                            ((dic['Comment']+';') if 'Comment' in dic else '') +\
                            ((dic['Comment'+'['+locale.getdefaultlocale()[0]+']'] + ';') if 'Comment'+'['+locale.getdefaultlocale()[0]+']' in dic else '')+\
                            ((dic['GenericName']+';') if 'GenericName' in dic else '') +\
                            ((dic['GenericName'+'['+locale.getdefaultlocale()[0]+']'] + ';') if 'GenericName'+'['+locale.getdefaultlocale()[0]+']' in dic else '')+\
                            ((dic['Categories']+';') if 'Categories' in dic else '')




class Searcher:
    def __init__(self):
        self.items = [Executable("/usr/share/applications/"+desktop) for desktop in os.listdir("/usr/share/applications") if desktop[-8:] == ".desktop"]
        self.items = sorted([app for app in self.items if app.Type == "Application"], key = lambda app: app.Name)

        # remove extra items with duplicate Exec
        execs = set()  # [app['Exec'] for app in self.items])
        items = []
        for item in self.items:
            if not (item.Name, item.Exec) in execs:
                items.append(item)
                execs.add((item.Name, item.Exec))
        self.items = items

    def getlist(self, keyword):
        '''
            result is a list of dictionaries:
                result[i]['Name']: app name
                result[i]['Comment']: app brief introduction
                result[i]['Exec']: app launch method
        '''
        rekw = keyword
        for char in "\/.+$^[](){}|":  # prevent the occurrence of user-input regular expressions
            rekw = rekw.replace(char, '\\'+char)
        rekw = '(.*?)(' + rekw.replace('*', '.*').replace('?', '.') + ')(.*?)'
        # replace with regular expressions
        result = sorted([dict({'Name': app.Name, 'Comment': app.Comment, 'Exec': app.Exec, 'Pos': re.match(rekw.lower(), app.Name.lower()).start(2)})
                         for app in self.items if re.match(rekw.lower(), app.Name.lower())],
                        key=lambda x: (x['Pos'], x['Name']))  # match position first, then dictionary order
        return result