#!/usr/bin/python3

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from sys import platform, exit
from os import path

import tkinter
import tkinter.scrolledtext as scrollText
from json import load


# Path of the file currently being edited
openFilePath = 'Untitled'

# used if there was a JSON error
jsonError = ''

# check platform the user is on
# these conditional statements are used to create a variable named commandKey.
# the variable 'commandKey' is used for determining if the user will be using 
# Command (if they are on mac) or Control (if they are not on mac)
if platform == 'darwin':
    # if the user is on mac use Command for keyboard shorcuts
    commandKey = 'Command'
else:
    # otherwise use Control for keyboard shortcuts
    commandKey = 'Control'


# main variable for the window
root = Tk()

# uses the derpy_pencil.png file as an icon (only works for Windows)
root.tk.call('wm', 
             'iconphoto',
             root._w, PhotoImage(file=path.dirname(path.abspath(__file__)) + '/derpy_pencil.png'))

# changes the minimum size of the window
root.minsize(450, 450)


# try to load the json settings
try:
    # create the variable settings for storing the settings of the editor
    settings = load(open(path.dirname(path.abspath(__file__)) + '/editorSettings.json', 'r'))

# if there is an error in editorSettings.json
# NOTE: If you are NOT familiar with JSON then you need to know that if the JSON syntax is done wrong then an error
# will be raised.
except Exception as err:
    exitRootButton = None

    # if there are errors then make the settings variable equal to some premade settings
    settings = {
        "fontName": "default",
        "fontSize": 12,
        "tabSize": 2,
        "backgroundColor": "white",
        "textColor": "black",
        "cursorColor": "black",
        "cursorStyle": "xterm",
        "ask before quit": "yes",
        "padx": 3,
        "pady": 1,
        "syntax": {}
    }
    jsonError = str(err) # used for line 431

# set the background color of root to the 'backgroundColor' item of settings
root.background = settings['backgroundColor']


# settings for the scrolledText widget. NOTE: the attributes of 'textArea' will rely on the settings dictonary.
textArea = scrollText.ScrolledText(
    root,
    font=(
        settings['fontName'],
        settings['fontSize']
    ),

    cursor=settings['cursorStyle'], # WARNING: if you do not know what you are doing this line of code can break the editor!
    background=settings['backgroundColor'],
    foreground=settings['textColor'],
    highlightcolor=settings['backgroundColor'],
    selectborderwidth=0,
    highlightthickness=0,
    padx=settings['padx'],
    pady=settings['pady'],
    undo=True
)

# this variable is used for a button that appears when the user opens up the manual or if there was a json error.
# The button is used for a user friendly exit.
exitButton = None

# change the cursor color of textArea to the item 'cursorColor' of settings
textArea.config(insertbackground=settings['cursorColor'])
textArea.pack(expand=True, fill='both') # make the editor area cover most of the screen

# make the title of the window the openFilePath
root.title(openFilePath)


# open a file
def openFile(event=None):
    # get global variables needed
    global textArea
    global openFilePath
    global exitButton

    # try to destroy the button.
    # A try and except statement is required here so that if 'exitButton' is not an actually a button the program
    # won't raise an error
    try:
        exitButton.destroy()
        exitButton = None
    except:
        exitButton = None

    # turn the 'textArea' widget to be read and write.
    # Needed becuase when the user looks at the manual the 'textArea' widget turns to be read only
    textArea.config(state=NORMAL)

    # open a dialog to open a file
    openFilePath = filedialog.askopenfilename()

    # try to open the file. If it does not work do nothing
    try:
        file = open(openFilePath, 'r')
        textArea.delete(1.0, "end-1c")
        textArea.insert(INSERT, file.read())
        file.close()
        root.title(openFilePath)
        high()
    except:
        return 'break'
    return 'break'


# create a new file
def newFile(event=None):
    # get global variables needed
    global exitButton
    global textArea
    global openFilePath
    global exitRootButton

    try:
        exitButton.destroy()
        exitButton = None
        exitRootButton.destroy()
        del exitRootButton
    except:
        exitButton = None

    textArea.config(state=NORMAL)
    openFilePath = 'Untitled'
    textArea.delete(1.0, "end-1c")
    root.title(openFilePath)
    return 'break'


# save to the current file
def saveFile(event=None):
    # get global variables needed
    global textArea
    global openFilePath

    # if the user is not editing a file then create a new one
    if openFilePath == 'Untitled':
        if saveAsFile() == False:
            return False
    if openFilePath == 'Manual':
        return True
    # if the user is editing the settings file save to 'editorSettings.py'
    elif openFilePath == 'Settings':
        file = open(path.dirname(path.abspath(__file__)) + '/editorSettings.json', 'w')
        file.write(str(textArea.get(1.0, "end-1c")))
        file.close()
        root.title('Settings')
    # otherwise save the file
    else:
        file = open(openFilePath, 'w')
        file.write(str(textArea.get(1.0, "end-1c")))
        file.close()
        root.title(openFilePath)
    return 'break'


# create a new file
def saveAsFile(event=None):
    # get global variables needed
    global textArea
    global openFilePath

    # if the file path is either 'Settings' or 'Manual' don't do anything
    # Otherwise ask to save as file
    if openFilePath == 'Settings':
        pass
    if openFilePath == 'Manual':
        pass
    else:
        file = filedialog.asksaveasfile(mode='w')
        if file is None:
            return False # needed when the user exits

        writeText = str(textArea.get(1.0, "end-1c"))
        file.write(writeText)
        file.close()

        openFilePath = file.name
        root.title(file.name)
    return 'break'


# open the userSettings file
def openSettingsFile():
    # get global variables needed
    global textArea
    global openFilePath
    global settingsState

    try:
        textArea.config(state=NORMAL)
        file = open(path.dirname(path.abspath(__file__)) + '/editorSettings.json', 'r')
        textArea.delete(1.0, "end-1c")
        textArea.insert(INSERT, file.read())
        file.close()
        openFilePath = 'Settings'
        root.title('Settings')
    except:
        return


# opens a window with instuctions on how to use the text editor
def showManual():
    # get global variables needed
    global textArea
    global openFilePath
    global exitButton

    manualFile = open(path.dirname(path.abspath(__file__)) + '/manual.txt', 'r')
    textArea.delete(1.0, "end-1c")
    textArea.insert(INSERT, manualFile.read())
    manualFile.close()
    exitButton = Button(root, text='Exit Manual', command = newFile)
    exitButton.pack()
    textArea.config(state=DISABLED)
    openFilePath = 'Manual'
    root.title(openFilePath)


# show a messagebox about the aplication
def showAbout():
    messagebox.showinfo('About', 'Author: John Paul Antonovich\n\nLicense: MIT\n\nDescription: '
        'A simple text editor built with Python and the Tkinter library. If you like to know more'
        ' read the README of this program!\n\n Repository: http://github.com/hatOnABox/'
        'Simple-Text-Editor')


# if the user tries to quit without saving ask them if they would like to save
# Note: if the function returns False then the window will not be destroyed.
# This is used becuase in earlier versions of this text editor would quit when the user never intended to quit.
def askQuit(event=None):
    if settings['ask before quit'] == 'no':
        root.quit()
    if openFilePath == 'Manual':
        return True
    if openFilePath == 'Settings':
        data = open(path.dirname(path.abspath(__file__)) + '/editorSettings.json').read()

        if data == str(textArea.get(1.0, "end-1c")):
            return True
        return messagebox.askyesno('Hold on!', 'Are you sure that you would like to quit?'
                                    ' You have changes that you haven\'t saved!')
    if openFilePath == 'Untitled':
        if messagebox.askyesno('Hold on!', 'Are you sure you would not like to save'
                                   ' \'Untitled\'?'):
            return True
        return saveFile()

    try:
        data = open(openFilePath).read()
        if data == str(textArea.get(1.0, "end-1c")):
            return True
        return messagebox.askyesno('Hold on!', 'Are you sure that you would like to quit? '
                                   'You have changes that you haven\'t saved!')
    except:
        return True


# syntax highlighting - I got this code from:
# https://stackoverflow.com/questions/29688831/pygments-syntax-highlighter-in-python-tkinter-text-widget
def highlightSyntax(word, color):
    textArea.tag_remove(word, 1.0, END)
    first = 1.0
    while True:
        first = textArea.search(r'{}'.format(str(word)), first, nocase=False, stopindex=END, regexp=False)
        if not first:
            break
        last = first + '+' + str(len(word)) + 'c'
        textArea.tag_add(word, first, last)
        first = last
    textArea.tag_config(word, foreground=str(color))


# run every time key is pressed
def high(event=None):
    if openFilePath == "Untitled":
        return
    filename, file_extension = path.splitext(openFilePath)
    for item in list(settings['syntax'].keys()):
        if item == file_extension:
            for key, value in settings['syntax'][item].items():
                highlightSyntax(key, value)
            break


# if tab is pressed enter the amount of space needed
def insertTab(event=None):
    textArea.insert(tkinter.INSERT, " " * settings['tabSize'])
    return 'break'


# used to break the program
def quit(event=None):
    if askQuit():
        root.quit()
        exit(0)


# redo command
def editRedo(event=None):
    try:
        textArea.edit_redo()
    except:
        pass


# undo command
def editUndo(event=None):
    try:
        textArea.edit_undo()
    except:
        pass


# copy command
def editCopy(event=None):
    try:
        root.clipboard_clear()
        root.clipboard_append(textArea.get('sel.first', 'sel.last'))
    except:
        pass


# cut command
def editCut(event=None):
    try:
        root.clipboard_clear()
        root.clipboard_append(textArea.get('sel.first', 'sel.last'))
        textArea.delete('sel.first', 'sel.last')
    except:
        pass


# paste command
def editPaste(event=None):
    textArea.insert(textArea.index(INSERT), root.clipboard_get())


menubar = Menu(root)

# create the 'file' menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='New  ' + commandKey + '-n', command=newFile)
filemenu.add_command(label='Open  ' + commandKey + '-o', command=openFile)
filemenu.add_command(label='Save  ' + commandKey + '-s', command=saveFile)
filemenu.add_command(label='Save As  ' + commandKey + '-Shift-S', command=saveAsFile)
filemenu.add_separator()
filemenu.add_command(label='Exit  ' + commandKey + '-q', command=quit)
menubar.add_cascade(label='File', menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label='Undo  ' + commandKey + '-u', command=editUndo)
editmenu.add_command(label='Redo  Shift-' + commandKey + '-u', command=editRedo)
editmenu.add_separator()
editmenu.add_command(label='Copy  ' + commandKey + '-c', command=editCopy)
editmenu.add_command(label='Cut  ' + commandKey + '-x', command=editCut)
editmenu.add_command(label='Paste  ' + commandKey + '-v', command=editPaste)
menubar.add_cascade(label='Edit', menu=editmenu)

# create the 'settings menu'
settingsmenu = Menu(menubar, tearoff=0)
settingsmenu.add_command(label='Open Prefrences', command=openSettingsFile)
menubar.add_cascade(label='Settings', menu=settingsmenu)

# create the 'help menu'
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='About', command=showAbout)
helpmenu.add_command(label='Manual', command=showManual)
menubar.add_cascade(label='Help', menu=helpmenu)

# add all of the menus to the window
root.config(menu=menubar)

# used for customized tabs
textArea.bind('<Tab>', insertTab)

# mac has a built in Command-q
if platform != 'darwin':
    root.bind('<' + commandKey + '-q>', quit)
else:
    root.createcommand('exit', quit)

# add keyboard shorcuts
textArea.bind('<Key>', high)
textArea.bind('<Shift-' + commandKey + '-z>', editRedo)
textArea.bind('<' + commandKey + '-n>', newFile)
textArea.bind('<' + commandKey + '-s>', saveFile)
textArea.bind('<' + commandKey + '-o>', openFile)
textArea.bind('<' + commandKey + '-Shift-S>', saveAsFile)

root.protocol("WM_DELETE_WINDOW", quit)

# if there was an json error
if jsonError != '':
    textArea.insert(INSERT, 'There was an error in the editorSettings.json file!\n\n' + str(jsonError))
    textArea.config(state=DISABLED)
    openFilePath = 'Oh, no! There was a Json error!'
    exitButton = Button(root, text='Got it!', command = newFile)
    exitRootButton = Button(root, text='Exit Application', fg='red', command = lambda: exit(0))
    exitButton.pack()
    exitRootButton.pack()
    root.title(openFilePath)

del jsonError # get rid of jsonError


def main():
    while True:
        root.mainloop()


if __name__ == '__main__':
    main()
