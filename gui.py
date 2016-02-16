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

		self.text_content = Text(dialogue, bd=0, bg="#333333", fg="#e29d36", height=12, state=NORMAL)
		self.text_content.pack(side=LEFT, fill=BOTH, expand=True)

		self.text_content.insert(END, "Hi, Peter," + '\n')
		self.text_content.insert(END, "How may I assist you?" + '\n')
		self.text_content.config(state=DISABLED)

		self.text_content.tag_configure('user', foreground="white")

		self.content_scroll = Scrollbar(dialogue, bd=0, command=self.text_content.yview)
		self.content_scroll.pack(side=RIGHT, fill=Y)
		self.text_content.config( yscrollcommand=self.content_scroll.set)

		# form
		form = Frame(self.parent, bg="white")
		form.pack(fill=BOTH, expand=True)

		self.input_content = StringVar()
		self.entry_main = Entry(form, bd=0)
		self.entry_main.bind('<Return>', self.callback)
		self.entry_main.pack(fill=X, padx=2, pady=2)

	# functionality
	def callback(self, event):
		self.text_content.config(state=NORMAL)
		self.input_content = self.entry_main.get()
		self.text_content.insert(END, self.input_content + '\n', ('user'))
		self.text_content.see(END)
		self.entry_main.delete(0, END)
		self.text_content.config(state=DISABLED)

		if 'vis' in self.input_content:
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, "No problem, let me crunch the numbers." + '\n')
			self.text_content.insert(END, "I'll show you all the rvs's waiting for approval" + '\n')
			self.text_content.insert(END, "since the last full report." + '\n')
			self.text_content.insert(END, "I won't log the data on this one." + '\n')
			self.text_content.see(END)
			self.text_content.config(state=DISABLED)
			self.after(500, self.vis)
		elif 'report' in self.input_content:
			self.report()

	def do_nothing(self):
		tkMessageBox.showinfo("Pointless Message", "I'm doing nothing")

	def do_not_do_something(event):
		print "I'm not doing anything"

	def quit(self):
		quit()

	def vis(self):
		# only at work
		root_dir = os.getcwd()
		os.chdir("..")
		subprocess.Popen(["python", "./RVS_vis.py"])
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
