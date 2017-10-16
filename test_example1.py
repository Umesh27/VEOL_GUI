__author__ = 'Umesh'

from tkinter import *

#------------------------------------

def addBox():
    print("ADD")

    ent = Entry(root)
    ent.pack()

    all_entries.append( ent )

#------------------------------------

def showEntries():

    for number, ent in enumerate(all_entries):
        print(number, ent.get())

#------------------------------------

#------------------------------------

def clearEntries():

    print("In clear entries :")
    # all_entries[i].delete(0, 'end')
    for i in range(len(all_entries)):
        print(i)
        all_entries[i].destroy()
#------------------------------------


all_entries = []

root = Tk()

showButton = Button(root, text='Show all text', command=showEntries)
showButton.pack()

addboxButton = Button(root, text='<Add Time Input>', fg="Red", command=addBox)
addboxButton.pack()

delButton = Button(root, text='clear entry', command=clearEntries)
delButton.pack()

root.mainloop()

#------------------------------------