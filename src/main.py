from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from sys import platform

import tkinter
import tkinter.scrolledtext as scrollText
from json import load


commandKey = ''
file_path = 'Untitled'

# check platform the user is on
if platform == 'darwin':
    # if the user is on mac use Command for keyboard shorcuts
    commandKey = 'Command'
else:
    # otherwise use Control for keyboard shortcuts
    commandKey = 'Control'


root = Tk()
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='src/derpy_pencil.png'))
root.minsize(450, 450)


# try to load the json settings
try:
    settings = load(open('src/editorSettings.json', 'r'))
# if there is an error
except Exception as err:
    settings = {
        "fontName": "default", 
        "fontSize": 12,
        "tabSize": 2,
        "backgroundColor": "white",
        "textColor": "black",
        "cursorColor": "black",
        "cursorStyle": "xterm",
        "ask before quit": "yes"
    }
    root.lower()
    messagebox.showinfo('Oh No!', 'There was an error in the editorSettings.json file! ' + str(err))

root.background = settings['backgroundColor']


# settings for the scrolledText widget
editArea = scrollText.ScrolledText(
    font=(
        settings['fontName'],
        settings['fontSize']
    ),
    
    cursor=settings['cursorStyle'],
    background=settings['backgroundColor'],
    foreground=settings['textColor'],
    highlightcolor=settings['backgroundColor'],
    selectborderwidth=0,
    highlightthickness=0,
    padx=3
)


editArea.config(insertbackground=settings['cursorColor'])
editArea.pack(expand=True, fill='both') # make the editor area cover most of the screen


root.title(file_path)


# open a file
def openFile(event=None):
    global editArea
    global file_path
    file_path = filedialog.askopenfilename()

    try:
        file = open(file_path, 'r')
        editArea.delete('1.0', "end-1c")
        editArea.insert(INSERT, file.read())
        file.close()
        root.title(file_path)
    except:
        return 'break'
    return 'break'


# save to the current file
def saveFile(event=None):
    global editArea
    global file_path

    # if the user is not editing a file then create a new one
    if file_path == 'Untitled':
        saveAsFile()
    # if the user is editing the settings file save to 'editorSettings.py'
    elif file_path == 'Settings':
        file = open('src/editorSettings.json', 'w')
        file.write(str(editArea.get(1.0, "end-1c")))
        file.close()
        root.title('Settings')
    # otherwise save the file
    else:
        file = open(str(file_path), 'w')
        file.write(str(editArea.get(1.0, "end-1c")))
        file.close()
        root.title(file_path)
    return 'break'


# if tab is pressed enter the amount of space needed
def insertTab(event=None):
    editArea.insert(tkinter.INSERT, " " * settings['tabSize'])
    return 'break'


# create a new file
def saveAsFile(event=None):
    global editArea
    global file_path
    
    if file_path == 'Settings':
        pass
    else:
        file = filedialog.asksaveasfile(mode='w')
        if file is None:
            return
        
        writeText = str(editArea.get(1.0, "end-1c"))
        file.write(writeText)
        file.close()

        file_path = file
        root.title(file.name)
    return 'break'


# open the userSettings file
def openSettingsFile():
    global editArea
    global file_path
    global settingsState

    try:
        file = open('src/editorSettings.json', 'r')
        editArea.delete(1.0, "end-1c")
        editArea.insert(INSERT, file.read())
        file.close()
        file_path = 'Settings'
        root.title('Settings')
    except:
        return


# show a messagebox about the aplication
def showAbout():
    messagebox.showinfo('About', 'Author: John Paul Antonovich\n\nLicense: MIT\n\nDescription: A simple text editor built with Python and the Tkinter library. If you like to know more read the README of this program!\n\n Repository: http://github.com/hatOnABox/Simple-Text-Editor')


# if the user tries to quit without saving ask them if they would like to save
def askQuit(event=None):
    if settings['ask before quit'] == 'no':
        root.quit()
    else:
        if file_path == 'Settings':
            data = open('src/editorSettings.json').read()
            
            if data != str(editArea.get(1.0, "end-1c")):
                if messagebox.askyesno('Hold on!', 'Are you sure that you would like to quit? You have changes that you haven\'t saved!') == True:
                    root.quit()
                else:
                    pass
            else:
                root.quit()
        elif file_path != 'Untitled':
            data = open(file_path).read()
            if data != str(editArea.get(1.0, "end-1c")):
                if messagebox.askyesno('Hold on!', 'Are you sure that you would like to quit? You have changes that you haven\'t saved!') == True:
                    root.quit()
                else:
                    pass
            else:
                root.quit()
        else:
            if messagebox.askyesno('Hold on!', 'Are you sure you would not like to save \'Untitled\'?') == True:
                root.quit()
            else:
                saveFile()      


# this is used becuase if the user uses control-q and the even is root.quit an error will be raised
def quit(event=None):
    root.quit()


menubar = Menu(root)

# create the 'file' menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open  ' + commandKey + '-o', command=openFile)
filemenu.add_command(label='Save  ' + commandKey + '-s', command=saveFile)
filemenu.add_command(label='Save As  ' + commandKey + '-Shift-S', command=saveAsFile)
filemenu.add_separator()
filemenu.add_command(label='Exit  ' + commandKey + '-q', command=askQuit)
menubar.add_cascade(label='File', menu=filemenu)

# create the 'settings menu'
settingsmenu = Menu(menubar, tearoff=0)
settingsmenu.add_command(label='Open Prefrences', command=openSettingsFile)
menubar.add_cascade(label='Settings', menu=settingsmenu)

# create the 'help menu'
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='About', command=showAbout)
menubar.add_cascade(label='Help', menu=helpmenu)

# add all of the menus to the window
root.config(menu=menubar)


# user can use Command-q or Control-q
root.bind('<' + commandKey + '-q>', quit)

# used for customized tabs
editArea.bind('<Tab>', insertTab)


# add keyboard shorcuts
editArea.bind('<' + commandKey + '-s>', saveFile)
editArea.bind('<' + commandKey + '-o>', openFile)
editArea.bind('<' + commandKey + '-Shift-S>', saveAsFile)


root.protocol("WM_DELETE_WINDOW",  askQuit)


def main():
    try:
        root.mainloop()
    except:
        askQuit()


if __name__ == '__main__':
    main()
