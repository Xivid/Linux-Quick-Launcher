from Tkinter import *
from functions import *
import subprocess

def run(app):
    subprocess.Popen(app,  shell = True)

def select(event):
    global entry_text, flag
    print apps.curselection(), event.keysym
    print flag
    if event.keysym == "Return" and sum != 0:
        subprocess.Popen(result[apps.curselection()[0]]["Exec"], shell = True)
        return
    elif event.keysym == "Escape":
        entry.focus_set()
        entry_text.set("")
        search()
    elif event.keysym == "Up" and (flag or sum == 1):
        entry.focus_set()
    elif event.keysym == "Up" and apps.curselection()[0] == 0:
        flag = True
        return
        
    flag = False

def input(event):
    global result, apps, entry_text, sum
    print event.keysym, event.keycode
    if event.keysym == "Return" and sum != 0:
        subprocess.Popen(result[0]["Exec"], shell = True)
        return
    elif event.keysym == "Escape":
        entry_text.set("")
    elif event.keysym == "Down":
        try:
            apps.focus_set()
            apps.bind("<KeyRelease>", select)
        except:
            pass
        return

    if event.keysym in ["Left", "Right", "Up", "Caps_Lock", "Num_Lock", "Delete", "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Super_L", "Super_R", "Home", "End", "Prior", "Next"]:
        return
    search()
        
def search():
    global result, apps, width, height, entry_text, sum
    
    kw = entry.get()
    try:
        apps.delete(0, apps.size())
        apps.destroy()
    except:
        pass
        
    if kw == ":q":
        root.destroy()

    result = searcher.getlist(kw)
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
            apps.insert(i, result[i]["Name"])
    else:
        root.geometry("{}x{}+0+0".format(width, 35))
        
result, apps = [], []
searcher = Searcher()
width, height = 240, 25
sum = 0
flag = False

root = Tk()

root.maxsize(width, 10 + height * 21)
root.minsize(240, 10 + height)
root.geometry("{}x{}+0+0".format(width, 35))

root.title("Linux Quick Launcher")

entry_text = StringVar()
entry = Entry(root, width = 32, textvariable = entry_text)
entry.place(x = 5, y = 5)
entry.bind("<KeyRelease>", input)
entry.focus_set()
root.mainloop()
