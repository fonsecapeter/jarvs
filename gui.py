#!/usr/bin/env python
# **** gui frame that does nothing ****
from Tkinter import *
import tkMessageBox
import os
import subprocess

# functionality

def do_nothing():
	tkMessageBox.showinfo("Pointless Message", "I'm doing nothing")

def do_not_do_something(event):
	print "I'm not doing anything"

def quit():
	root.quit()

def vis():
	# only at work
	root_dir = os.getcwd()
	os.chdir("..")
	exec(open("./RVS_vis.py").read(), globals())
	os.chdir(root_dir)

def report():
	# only at work
	root_dir = os.getcwd()
	os.chdir("..")
	subprocess.call("./RVS_reporter.sh", shell=True)
	os.chdir(root_dir)

# gui

root = Tk()
root.wm_title("Jarvs Gui")

# main men with dropdowns

main_menu = Menu(root, bd=0, activeborderwidth=0)
root.config(menu=main_menu) # tkinter does everything!

file_menu = Menu(main_menu, bd=0, activeborderwidth=0)
main_menu.add_cascade(label="file", menu=file_menu)
file_menu.add_command(label="Quick visual", command=vis)
file_menu.add_command(label="Full report", command=report)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit)

edit_menu = Menu(main_menu, bd=0, activeborderwidth=0)
main_menu.add_cascade(label="edit", menu=edit_menu)
edit_menu.add_command(label="Redo", command=do_nothing)

# form
form = Frame(root, bg="white")

label_1 = Label(form, text="Hi, Peter,", anchor=W, bg="white")
label_2 = Label(form, text="How many I assist you?", anchor=W, bg="white")
entry_1 = Entry(form, bd=0)

label_1.grid(row=0, column=0, sticky=W)
label_2.grid(row=1, column=0, sticky=W)
entry_1.grid(row=2, column=0, padx=2, pady=2)

# functional button
button_1 = Button(form, text="Enter", bd=0, bg="white")
button_1.bind("<Button-1>", do_not_do_something) # lclick = <Button-1>, mclick = <Button-2>, lclick = <Button-3>
button_1.grid(row=3, column=0, padx=2, pady=2)

form.pack(fill=BOTH)

# status bar
##status = Label(root, text="Preparing to do nothing", bg="white", anchor=W) # anchor is text align, N E S W
##status.pack(side=BOTTOM, fill=X)

root.mainloop()