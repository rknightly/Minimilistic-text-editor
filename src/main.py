from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrollText
from tkinter import filedialog
from sys import platform

commandKey = ''
file_path = 'Untitled'


if platform == 'darwin':
    commandKey = 'Command'
else:
    commandKey = 'Control'


root = Tk()
editArea = scrollText.ScrolledText(width=450, height=420)
editArea.pack()


root.title(file_path)


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
        return


def saveFile(event=None):
    global editArea
    global file_path

    if file_path == 'Untitled':
        saveAsFile()
    else:
        file = open(file_path, 'w')
        file.write(str(editArea.get(1.0, END)))
        file.close()
        root.title(file_path)


def saveAsFile():
    global editArea
    global file_path

    file = filedialog.asksaveasfile(mode='w')
    if file is None:
        return
    
    writeText = str(editArea.get(1.0, END))
    file.write(writeText)
    file.close()

    file_path = file
    root.title(file.name)


def showAbout():
    messagebox.showinfo('About', 'Author: John Paul Antonovich\n\nDescription: A simple text editor built with Python and the Tkinter library.')



menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open  ' + commandKey + '-o', command=openFile)
filemenu.add_command(label='Save  ' + commandKey + '-s', command=saveFile)
filemenu.add_command(label='Save As  ' + commandKey + '-Shift-S', command=saveAsFile)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
menubar.add_cascade(label='File', menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label='About', command=showAbout)
menubar.add_cascade(label='Help', menu=helpmenu)

root.config(menu=menubar)


root.bind('<' + commandKey + '-s>', saveFile)
root.bind('<' + commandKey + '-o>', openFile)
root.bind('<' + commandKey + '-Shift-S>', saveAsFile)



root.minsize(450, 420)
root.maxsize(450, 420)
root.mainloop()
