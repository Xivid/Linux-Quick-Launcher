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

        # desktop application list
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

        # system directories
        self.syslist = []
        dirlist = ['/bin/', '/usr/bin/', '/usr/local/bin/']
        for dir in dirlist:
            self.syslist += self.getcommand(dir)
        # print len(self.syslist), 'items found in system directories.'

        #filesystem
        self.xlist = self.syslist

    def getcommand(self, directory, root = False):
        """
        Get the filename('Name') and path('Exec') of all executable files in a given directory and its sub-directories.
        Recursive function. Very slow.
        :param directory: complete path of a directory
        :return: a list of dictionaries with ['Name'], ['Exec'], ['Comment']
        """
        retlist = []
        os.chdir(directory)
        for filename in os.listdir(directory):
            if (not os.path.islink(filename)) and os.path.isdir(filename):
                retlist += self.getcommand(directory+filename+'/')
                os.chdir(directory)
            elif os.system('if [ -x "{}" ]; then return 1; else return 0; fi'.format(filename)) == 256:
                retlist.append(dict({"Name": filename, 'Comment': directory + filename,
                                     "Exec": ('xterm -hold -e sudo ' if root else 'xterm -hold -e ') + directory + filename}))
        return retlist

    def refy(self, keyword):
        # replace with regular expressions
        rekw = keyword
        for char in "\/.+$^[](){}|":  # prevent the occurrence of user-input regular expressions
            rekw = rekw.replace(char, '\\'+char)
        rekw = '(.*?)(' + rekw.replace('*', '.*').replace('?', '.') + ')(.*?)'
        return rekw

    def getlist(self, keyword):
        """
            :param keyword: User typed-in keyword referring to some desktop application.
            :return:
            result is a list of dictionaries:
                result[i]['Name']: app name
                result[i]['Comment']: app brief introduction
                result[i]['Exec']: app launch method
        """
        if keyword[:4] == ':sys':
            return self.getsys(keyword.split(' ', 1)[1].strip())
        elif keyword[:2] == ':x':
            if self.xlist == self.syslist:
                dirlist = ['/bin/', '/boot/', '/home/', '/opt/', '/usr/']
                for dir in dirlist:
                    self.xlist += self.getcommand(dir)
                dirlist = ['/sbin/', '/usr/sbin/', '/usr/local/sbin/']  # commands here requires root permission
                for dir in dirlist:
                    self.xlist += self.getcommand(dir, root = 'True')
                print len(self.xlist), 'items found in the filesystem.'
            return self.getx(keyword.split(' ', 1)[1].strip())

        # default(only desktop applications)
        rekw = self.refy(keyword)
        result = sorted([dict({'Name': app.Name, 'Comment': app.Comment, 'Exec': app.Exec, 'Pos': re.match(rekw.lower(), app.Name.lower()).start(2)})
                         for app in self.items if re.match(rekw.lower(), app.Name.lower())],
                        key=lambda x: (x['Pos'], x['Name']))  # match position first, then dictionary order
        return result

    def getsys(self, keyword):
        """
        :param keyword: The program name the user wants, with prefix ':sys' deleted.
        :return:
            A list of dictionaries:
                result[i]['Name']: program filename
                result[i]['Exec']: launch command
            The programs exists in:
                /bin
                /usr/bin
                /usr/local/bin
        """
        #uses self.syslist[i]['Name']&['Exec']
        rekw = self.refy(keyword)
        return sorted([dict(dict({'Pos': re.match(rekw.lower(), comm['Name'].lower()).start(2)}), **comm)
                        for comm in self.syslist if re.match(rekw.lower(), comm['Name'].lower())],
                      key = lambda x: (x['Pos'], x['Name']))  # match position first, then dictionary order

    def getx(self, keyword):
        """
        :param keyword:
        :return:
            Another list of more dictionaries.
            The programs exists in:
            /bin
            /boot
            /home
            /opt
            /usr
            especially(sudo) /sbin; /usr/sbin; /usr/local/sbin
        """
        rekw = self.refy(keyword)
        return sorted([dict(dict({'Pos': re.match(rekw.lower(), comm['Name'].lower()).start(2)}), **comm)
                        for comm in self.xlist if re.match(rekw.lower(), comm['Name'].lower())],
                      key = lambda x: (x['Pos'], x['Name']))  # match position first, then dictionary order

searcher = Searcher()