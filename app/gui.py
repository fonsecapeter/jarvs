#!/usr/bin/env python
# import standard & 3rd party libraries
from Tkinter import *
import tkMessageBox
import tkColorChooser
import os
import subprocess
import time
import sqlite3 as sql
from PIL import Image, ImageTk
# import jarvs-specific methods
import rvspracticedata as rvsdata
import jarvisms
import attendingsgui
import preferencesgui

class Jarvs(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)

		self.parent = parent
		self.init_ui()

	def init_ui(self):

		self.parent.title("Jarvs")
		self.pack(fill=BOTH, expand=True)

		# main menu with dropdowns

		main_menu = Menu(self.parent, bd=0, activeborderwidth=0)
		self.parent.config(menu=main_menu) # tkinter does everything!

		jarvs_menu = Menu(main_menu, bd=0, activeborderwidth=0)
		main_menu.add_cascade(label="jarvs", menu=jarvs_menu)
		jarvs_menu.add_command(label="Preferences", command=self.set_preferences)
		jarvs_menu.add_command(label="Attendings", command=lambda: self.set_attendings("real"))
		jarvs_menu.add_separator()
		jarvs_menu.add_command(label="Quick visual", command=self.vis)
		jarvs_menu.add_command(label="Full report", command=self.report)
		jarvs_menu.add_command(label="Test email", command=self.test_email)
		jarvs_menu.add_command(label="Full email", command=self.email)
		jarvs_menu.add_separator()
		jarvs_menu.add_command(label="Exit", command=self.end_jarvs)

		practice_menu = Menu(main_menu, bd=0, activeborderwidth=0)
		main_menu.add_cascade(label="practice", menu=practice_menu)
		practice_menu.add_command(label="Attendings", command=lambda: self.set_attendings("practice"))
		practice_menu.add_separator()
		practice_menu.add_command(label="Quick visual", command=self.practice_vis)
		practice_menu.add_command(label="Full report", command=self.practice_report)
		practice_menu.add_command(label="Test email", command=self.practice_test_email)
		practice_menu.add_command(label="Full email", command=self.practice_email)
		practice_menu.add_separator()
		practice_menu.add_command(label="Practice set up", command=self.practice_setup)

		# dialogue
		dialogue = Frame(self.parent)
		dialogue.pack(fill=BOTH, expand=True)

		self.text_content = Text(dialogue, bd=0, highlightthickness=0, bg=rvsdata.background_color, fg=rvsdata.jarvs_color, height=12, state=NORMAL)
		self.text_content.pack(side=LEFT, fill=BOTH, expand=True)

		self.text_content.insert(END, jarvisms.greeting_1() + '\n')
		self.text_content.insert(END, jarvisms.greeting_2() + '\n')
		self.text_content.config(state=DISABLED)

		self.text_content.tag_configure('user', foreground=rvsdata.user_color)

		self.content_scroll = Scrollbar(dialogue, bd=0, command=self.text_content.yview, bg=rvsdata.background_color, troughcolor=rvsdata.background_color, highlightthickness=0, activebackground=rvsdata.jarvs_color)
		##self.content_scroll.pack(side=RIGHT, fill=Y)
		self.text_content.config( yscrollcommand=self.content_scroll.set)

		# form
		self.form = Frame(self.parent, bg=rvsdata.background_color, bd=0)
		self.form.pack(fill=BOTH, expand=True)

		self.input_content = StringVar()
		self.entry_main = Entry(self.form, fg=rvsdata.user_color, bg=rvsdata.background_color, insertbackground=rvsdata.user_color, highlightthickness=0, bd=0)
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

		if 'preferences' in self.input_content:
			self.set_preferences()
		elif 'attending' in self.input_content:
			self.set_attendings("real")
		elif 'practice' in self.input_content:
			if 'attending' in self.input_content:
				self.set_attendings("practice")
			elif 'vis' in self.input_content:
				self.text_content.config(state=NORMAL)
				self.text_content.insert(END, "No problem, let me crunch the numbers." + '\n')
				self.text_content.insert(END, "I'll show you all the practice rvs's waiting for" + '\n')
				self.text_content.insert(END, "approval since the last full report." + '\n')
				self.text_content.insert(END, "I won't log the data on this one." + '\n')
				self.text_content.see(END)
				self.text_content.config(state=DISABLED)
				self.after(500, self.practice_vis)
			elif 'report' in self.input_content:
				self.text_content.config(state=NORMAL)
				self.text_content.insert(END, "No problem, let me crunch the numbers." + '\n')
				self.text_content.insert(END, "I'll show you all the practice rvs's currently" + '\n')
				self.text_content.insert(END, "waiting for approval." + '\n')
				self.text_content.insert(END, "I will log the data on this one." + '\n')
				self.text_content.see(END)
				self.text_content.config(state=DISABLED)
				self.after(500, self.practice_report)
		elif 'vis' in self.input_content:
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, "No problem, let me crunch the numbers." + '\n')
			self.text_content.insert(END, "I'll show you all the rvs's waiting for approval" + '\n')
			self.text_content.insert(END, "since the last full report." + '\n')
			self.text_content.insert(END, "I won't log the data on this one." + '\n')
			self.text_content.see(END)
			self.text_content.config(state=DISABLED)
			self.after(500, self.vis)
		elif 'report' in self.input_content:
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, "No problem, let me crunch the numbers." + '\n')
			self.text_content.insert(END, "I'll show you all the rvs's currently waiting" + '\n')
			self.text_content.insert(END, "for approval." + '\n')
			self.text_content.insert(END, "I will log the data on this one." + '\n')
			self.text_content.see(END)
			self.text_content.config(state=DISABLED)
			self.after(500, self.report)
		elif 'bye' in self.input_content:
			self.end_jarvs()
		# conversational only
		elif 'thank' in self.input_content:
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, jarvisms.yourewelcome() + '\n')
		elif 'you' in self.input_content:
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, jarvisms.thankyou() + '\n')
		else:
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, jarvisms.response() + '\n')

	def do_nothing(self):
		tkMessageBox.showinfo("Pointless Message", "I'm doing nothing")

	def end_jarvs(self):
		self.text_content.config(state=NORMAL)
		self.text_content.insert(END, jarvisms.signoff() + '\n')
		self.text_content.see(END)
		self.text_content.config(state=DISABLED)
		self.update()
		time.sleep(1)
		quit()

	def set_preferences(self):
		preferencesgui.main(self)
		init_vars()

	def set_attendings(self, database):
		attendingsgui.main(self, "practice")
		init_vars()

	# <--- rvs functionality --->
	# only at work with scripts one dir back from jarvs
	def vis(self):
		root_dir = os.getcwd()
		os.chdir("../..")
		subprocess.Popen(["python", "./RVS_vis.py"])
		os.chdir(root_dir)

	def report(self):
		root_dir = os.getcwd()
		os.chdir("../..")
		subprocess.Popen(["./RVS_reporter.sh"], shell=True)
		os.chdir(root_dir)

	def email(self):
		root_dir = os.getcwd()
		os.chdir("../..")
		subprocess.Popen(["./RVS_emailer.sh"], shell=True)
		os.chdir(root_dir)

	def test_email(self):
		root_dir = os.getcwd()
		os.chdir("../..")
		subprocess.Popen(["./RVS_test_emailer.sh"], shell=True)
		os.chdir(root_dir)

	# practice in app
	def practice_vis(self):
		root_dir = os.getcwd()
		os.chdir("./rvs")
		subprocess.Popen(["python", "./RVS_vis.py"])
		os.chdir(root_dir)

	def practice_report(self):
		root_dir = os.getcwd()
		os.chdir("./rvs")
		subprocess.Popen(["./RVS_reporter.sh"], shell=True)
		os.chdir(root_dir)

	def practice_email(self):
		root_dir = os.getcwd()
		os.chdir("./rvs")
		subprocess.Popen(["./RVS_emailer.sh"], shell=True)
		os.chdir(root_dir)

	def practice_test_email(self):
		root_dir = os.getcwd()
		os.chdir("./rvs")
		subprocess.Popen(["./RVS_test_emailer.sh"], shell=True)
		os.chdir(root_dir)

	def practice_setup(self):
		root_dir = os.getcwd()
		os.chdir("./rvs")
		subprocess.Popen(["./RVS_test_setup.sh"], shell=True)
		os.chdir(root_dir)

# run gui

def init_vars():
	reload(rvsdata)

	global gray_color
	gray_color = '#eeeeee'
	global dark_gray_color
	dark_gray_color = '#e6e6e6'

def main():
	init_vars()
	root = Tk()
	app_main = Jarvs(root)
	root.mainloop()

# conditionally execute script or as module if imported elsewhere
if __name__ == '__main__':
	main()
