#!/usr/bin/env python
# **** gui frame that does nothing ****
from Tkinter import *
import tkMessageBox
import os
import subprocess

class Jarvs(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.init_ui()

	def init_ui(self):

		self.parent.title("Jarvs Gui")
		self.pack(fill=BOTH, expand=True)
		self.var = BooleanVar()

		# main men with dropdowns

		main_menu = Menu(self.parent, bd=0, activeborderwidth=0)
		self.parent.config(menu=main_menu) # tkinter does everything!

		file_menu = Menu(main_menu, bd=0, activeborderwidth=0)
		main_menu.add_cascade(label="file", menu=file_menu)
		file_menu.add_command(label="Quick visual", command=self.vis)
		file_menu.add_command(label="Full report", command=self.report)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=self.quit)

		edit_menu = Menu(main_menu, bd=0, activeborderwidth=0)
		main_menu.add_cascade(label="edit", menu=edit_menu)
		edit_menu.add_command(label="Redo", command=self.do_nothing)

		# dialogue
		dialogue = Frame(self.parent)
		dialogue.pack(fill=BOTH, expand=True)

		self.text_content = Text(dialogue)
		self.text_content.pack()

		# form
		form = Frame(self.parent, bg="white")
		form.pack(fill=BOTH, expand=True)

		label_1 = Label(form, text="Hi, Peter,", anchor=W, bg="white")
		label_2 = Label(form, text="How many I assist you?", anchor=W, bg="white")

		label_1.grid(row=0, column=0, sticky=W)
		label_2.grid(row=1, column=0, sticky=W)

		self.input_content = StringVar()
		self.entry_main = Entry(form, bd=0)
		self.entry_main.grid(row=2, column=0, padx=2, pady=2)

		# functional button
		button_1 = Button(form, text="Enter", bd=0, bg="white", command=self.callback)
		##button_1.bind("<Button-1>", self.do_not_do_something) # lclick = <Button-1>, mclick = <Button-2>, lclick = <Button-3>
		button_1.grid(row=3, column=0, padx=2, pady=2)


		# status bar
		##status = Label(self, text="Preparing to do nothing", bg="white", anchor=W) # anchor is text align, N E S W
		##status.pack(side=BOTTOM, fill=X)

		# test dynamic check button
		cb = Checkbutton(form, text="show title", variable=self.var, command=self.toggle_title)
		cb.select()
		cb.grid(row=4, column=0, columnspan=2, padx=2, pady=2)

	# functionality
	def callback(self):
		self.input_content = self.entry_main.get()
		self.text_content.insert(END, self.input_content + '\n')

	def toggle_title(self):
		if self.var.get() == True:
			self.master.title("Jarvs Gui")
		else:
			self.master.title("")

	def do_nothing(self):
		tkMessageBox.showinfo("Pointless Message", "I'm doing nothing")

	def do_not_do_something(event):
		print "I'm not doing anything"

	def quit(self):
		self.quit()

	def vis(self):
		# only at work
		root_dir = os.getcwd()
		os.chdir("..")
		exec(open("./RVS_vis.py").read(), globals())
		os.chdir(root_dir)

	def report(self):
		# only at work
		root_dir = os.getcwd()
		os.chdir("..")
		subprocess.call("./RVS_reporter.sh", shell=True)
		os.chdir(root_dir)


# run gui

def main():
	root = Tk()
	app = Jarvs(root)
	root.mainloop()

# conditionally execute script or as module if imported elsewhere
if __name__ == '__main__':
	main()
