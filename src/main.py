from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from sys import platform
from os import system

import tkinter
import tkinter.scrolledtext as scrollText
import json

commandKey = ''
file_path = 'Untitled'

# check platform the user is on
if platform == 'darwin':
    # if the user is on mac use Command for keyboard shorcuts
    commandKey = 'Command'
else:
    # otherwise use Control for keyboard shortcuts
    commandKey = 'Control'


settings = json.load(open('src/editorSettings.json', 'r'))

root = Tk()
root.background = settings['backgroundColor']

# settings for the scrolledText widget
editArea = scrollText.ScrolledText(
    font=(
        settings['fontName'],
        settings['fontSize']
    ),
    
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
        editArea.delete('1.0', END)
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
        file = open('src/editorSettings.py', 'w')
        file.write(str(editArea.get(1.0, END)))
        file.close()
        root.title('Settings')
    # otherwise save the file
    else:
        file = open(str(file_path), 'w')
        file.write(str(editArea.get(1.0, END)))
        file.close()
        root.title(file_path)


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
        
        writeText = str(editArea.get(1.0, END))
        file.write(writeText)
        file.close()

        file_path = file
        root.title(file.name)


# open the userSettings file
def openSettingsFile():
    global editArea
    global file_path
    global settingsState

    try:
        file = open('src/editorSettings.json', 'r')
        editArea.delete('1.0', END)
        editArea.insert(INSERT, file.read())
        file.close()
        file_path = 'Settings'
        root.title('Settings')
    except:
        return


# show a messagebox about the aplication
def showAbout():
    messagebox.showinfo('About', 'Author: John Paul Antonovich\n\nLicense: MIT\n\nDescription: A simple text editor built with Python and the Tkinter library.')


menubar = Menu(root)

# create the 'file' menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open  ' + commandKey + '-o', command=openFile)
filemenu.add_command(label='Save  ' + commandKey + '-s', command=saveFile)
filemenu.add_command(label='Save As  ' + commandKey + '-Shift-S', command=saveAsFile)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
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

# used for customized tabs
editArea.bind('<Tab>', insertTab)



# add keyboard shorcuts
editArea.bind('<' + commandKey + '-s>', saveFile)
editArea.bind('<' + commandKey + '-o>', openFile)
editArea.bind('<' + commandKey + '-Shift-S>', saveAsFile)


root.minsize(450, 450)


def main():
    try:
        root.mainloop()
    except:
        pass # this code is only here if the user keyboardInturrupts the program 



if __name__ == '__main__':
    main()

