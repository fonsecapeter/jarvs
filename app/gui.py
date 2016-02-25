#!/usr/bin/env python
# import 3rd party libraries
from Tkinter import *
import tkMessageBox
import os
import subprocess
import time
import dataset
import json
# import jarvs-specific methods
import jarvisms

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
		jarvs_menu.add_command(label="Quick visual", command=self.vis)
		jarvs_menu.add_command(label="Full report", command=self.report)
		jarvs_menu.add_command(label="Test email", command=self.test_email)
		jarvs_menu.add_command(label="Full email", command=self.email)
		jarvs_menu.add_separator()
		jarvs_menu.add_command(label="Exit", command=self.end_jarvs)

		practice_menu = Menu(main_menu, bd=0, activeborderwidth=0)
		main_menu.add_cascade(label="practice", menu=practice_menu)
		practice_menu.add_command(label="Attendings", command=self.set_attendings)
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

		self.text_content = Text(dialogue, bd=0, highlightthickness=0, bg=background_color, fg=jarvs_color, height=12, state=NORMAL)
		self.text_content.pack(side=LEFT, fill=BOTH, expand=True)

		self.text_content.insert(END, jarvisms.greeting_1() + '\n')
		self.text_content.insert(END, jarvisms.greeting_2() + '\n')
		self.text_content.config(state=DISABLED)

		self.text_content.tag_configure('user', foreground=user_color)

		self.content_scroll = Scrollbar(dialogue, bd=0, command=self.text_content.yview, bg=background_color, troughcolor=background_color, highlightthickness=0, activebackground=jarvs_color)
		self.content_scroll.pack(side=RIGHT, fill=Y)
		self.text_content.config( yscrollcommand=self.content_scroll.set)

		# form
		form = Frame(self.parent, bg=background_color, bd=0)
		form.pack(fill=BOTH, expand=True)

		self.input_content = StringVar()
		self.entry_main = Entry(form, fg=user_color, bg=background_color, insertbackground=user_color, highlightthickness=0, bd=0)
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
			self.text_content.config(state=NORMAL)
			self.text_content.insert(END, "No problem, let me crunch the numbers." + '\n')
			self.text_content.insert(END, "I'll show you all the rvs's currently waiting" + '\n')
			self.text_content.insert(END, "for approval." + '\n')
			self.text_content.insert(END, "I will log the data on this one." + '\n')
			self.text_content.see(END)
			self.text_content.config(state=DISABLED)
			self.after(500, self.report)
		elif 'preferences' in self.input_content:
			self.set_preferences()
		elif 'bye' in self.input_content:
			self.end_jarvs()

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

	# <--- preferences --->
	def set_preferences(self):
		init_vars()
		prefs = Toplevel(self.parent)
		prefs.wm_title("Jarvs Preferences")
		prefs_window = Frame(prefs)
		prefs_window.pack(fill=BOTH, expand=True)

		# user_name
		self.user_name_label = Label(prefs_window, text="User Name: ")
		self.user_name_label.grid(row=0, column=0, sticky=E, padx=2, pady=2)
		self.user_name_entry = Entry(prefs_window, bd=0)
		self.user_name_entry.insert(END, user_name)
		self.user_name_entry.grid(row=0, column=1, padx=2, pady=2)
		self.user_name_entry.bind('<Return>', self.save_user_name)

		# email
		self.user_email_label = Label(prefs_window, text="User Email: ")
		self.user_email_label.grid(row=1, column=0, sticky=E, padx=2, pady=2)
		self.user_email_entry = Entry(prefs_window, bd=0)
		self.user_email_entry.insert(END, user_email)
		self.user_email_entry.grid(row=1, column=1, padx=2, pady=2)
		self.user_email_entry.bind('<Return>', self.save_user_email)

		# color
		self.user_color_label = Label(prefs_window, text="User Color: ")
		self.user_color_label.grid(row=2, column=0, sticky=E, padx=2, pady=2)
		self.user_color_entry = Entry(prefs_window, bd=0)
		self.user_color_entry.insert(END, user_color)
		self.user_color_entry.grid(row=2, column=1, padx=2, pady=2)
		self.user_color_entry.bind('<Return>', self.save_user_color)

		self.jarvs_color_label = Label(prefs_window, text="Jarvs Color: ")
		self.jarvs_color_label.grid(row=3, column=0, sticky=E, padx=2, pady=2)
		self.jarvs_color_entry = Entry(prefs_window, bd=0)
		self.jarvs_color_entry.insert(END, jarvs_color)
		self.jarvs_color_entry.grid(row=3, column=1, padx=2, pady=2)
		self.jarvs_color_entry.bind('<Return>', self.save_jarvs_color)

		self.background_color_label = Label(prefs_window, text="Background Color: ")
		self.background_color_label.grid(row=4, column=0, sticky=E, padx=2, pady=2)
		self.background_color_entry = Entry(prefs_window, bd=0)
		self.background_color_entry.insert(END, background_color)
		self.background_color_entry.grid(row=4, column=1, padx=2, pady=2)
		self.background_color_entry.bind('<Return>', self.save_background_color)

		self.color_label = Label(prefs_window, text="( enter color as name or hex )")
		self.color_label.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

		# save all button
		self.save_prefs_button = Button(prefs_window, text="Save", bd=0)
		self.save_prefs_button.bind('<Button-1>', self.save_all_preferences)
		self.save_prefs_button.grid(row=6, column=0, columnspan=2, padx=2, pady=2)

	# unit saves
	def save_user_name(self, event):
		self.user_name_shell = "echo " + self.user_name_entry.get().rstrip() + " > ./preferences/user_name.txt"
		os.system(self.user_name_shell)

		Preferences_Table.update(dict(ID=0, USERNAME=self.user_name_entry.get().rstrip()), ['ID'])

	def save_user_email(self, event):
		self.user_email_shell = "echo " + self.user_email_entry.get().rstrip() + " > ./preferences/user_email.txt"
		os.system(self.user_email_shell)

		Preferences_Table.update(dict(ID=0, USEREMAIL=self.user_email_entry.get().rstrip()), ['ID'])

	def save_user_color(self, event):
		self.user_color_shell = "echo " + self.user_color_entry.get().rstrip() + " > ./preferences/user_color.txt"
		os.system(self.user_color_shell)

		Preferences_Table.update(dict(ID=0, USERCOLOR=self.user_color_entry.get().rstrip()), ['ID'])

	def save_jarvs_color(self, event):
		self.jarvs_color_shell = "echo " + self.jarvs_color_entry.get().rstrip() + " > ./preferences/jarvs_color.txt"
		os.system(self.jarvs_color_shell)

		Preferences_Table.update(dict(ID=0, JARVSCOLOR=self.jarvs_color_entry.get().rstrip()), ['ID'])

	def save_background_color(self, event):
		self.background_color_shell = "echo " + self.background_color_entry.get().rstrip() + " > ./preferences/background_color.txt"
		os.system(self.background_color_shell)

		Preferences_Table.update(dict(ID=0, BACKGROUNDCOLOR=self.background_color_entry.get().rstrip()), ['ID'])

	# save all

	def save_all_preferences(self, event):
		self.save_user_name(event)
		self.save_user_email(event)
		self.save_user_color(event)
		self.save_jarvs_color(event)
		self.save_background_color(event)
		init_vars()
		self.text_content.configure(fg=jarvs_color, bg=background_color)
		self.text_content.tag_configure('user', foreground=user_color)
		self.update()

	# <--- edit and display attendings data --->
	def populate_attends_list(self):
		for Attending in attending_ids:
			jdump = json.dumps(Attendings_Table.find_one(ID=Attending))
			jdata = json.loads(jdump)
			#self.attends_list.insert(Attending, json.dumps(Attendings_Table.find_one(ID=Attending), separators=('  ', ': ')))
			self.attends_list_id.insert(Attending, jdata['ID'])

		for Attending in attending_ids:
			jdump = json.dumps(Attendings_Table.find_one(ID=Attending))
			jdata = json.loads(jdump)
			#self.attends_list.insert(Attending, json.dumps(Attendings_Table.find_one(ID=Attending), separators=('  ', ': ')))
			self.attends_list_fname.insert(Attending, jdata['FNAME'])

		for Attending in attending_ids:
			jdump = json.dumps(Attendings_Table.find_one(ID=Attending))
			jdata = json.loads(jdump)
			#self.attends_list.insert(Attending, json.dumps(Attendings_Table.find_one(ID=Attending), separators=('  ', ': ')))
			self.attends_list_lname.insert(Attending, jdata['LNAME'])

		for Attending in attending_ids:
			jdump = json.dumps(Attendings_Table.find_one(ID=Attending))
			jdata = json.loads(jdump)
			#self.attends_list.insert(Attending, json.dumps(Attendings_Table.find_one(ID=Attending), separators=('  ', ': ')))
			self.attends_list_dirname.insert(Attending, jdata['DIRNAME'])

		for Attending in attending_ids:
			jdump = json.dumps(Attendings_Table.find_one(ID=Attending))
			jdata = json.loads(jdump)
			#self.attends_list.insert(Attending, json.dumps(Attendings_Table.find_one(ID=Attending), separators=('  ', ': ')))
			self.attends_list_email.insert(Attending, jdata['EMAIL'])

		# colorize alternating rows
		for Row in range(0, len(db['Attendings']), 2):
			self.attends_list_id.itemconfigure(Row, background='#e6e6e6')
			self.attends_list_fname.itemconfigure(Row, background='#e6e6e6')
			self.attends_list_lname.itemconfigure(Row, background='#e6e6e6')
			self.attends_list_dirname.itemconfigure(Row, background='#e6e6e6')
			self.attends_list_email.itemconfigure(Row, background='#e6e6e6')

	def display_attends_entry(self, index):
		self.attends_list_id_content = self.attends_list_id.get(index)
		self.attends_id_entry.delete(0, END)
		self.attends_id_entry.insert(END, self.attends_list_id_content)

		self.attends_list_fname_content = self.attends_list_fname.get(index)
		self.attends_fname_entry.delete(0, END)
		self.attends_fname_entry.insert(END, self.attends_list_fname_content)

		self.attends_list_lname_content = self.attends_list_lname.get(index)
		self.attends_lname_entry.delete(0, END)
		self.attends_lname_entry.insert(END, self.attends_list_lname_content)

		self.attends_list_dirname_content = self.attends_list_dirname.get(index)
		self.attends_dirname_entry.delete(0, END)
		self.attends_dirname_entry.insert(END, self.attends_list_dirname_content)

		self.attends_list_email_content = self.attends_list_email.get(index)
		self.attends_email_entry.delete(0, END)
		self.attends_email_entry.insert(END, self.attends_list_email_content)

	def get_attends_list_id(self, event):
		attends_list_index = self.attends_list_id.curselection()[0]
		self.display_attends_entry(attends_list_index)

	def get_attends_list_fname(self, event):
		attends_list_index = self.attends_list_fname.curselection()[0]
		self.display_attends_entry(attends_list_index)

	def get_attends_list_lname(self, event):
		attends_list_index = self.attends_list_lname.curselection()[0]
		self.display_attends_entry(attends_list_index)

	def get_attends_list_dirname(self, event):
		attends_list_index = self.attends_list_dirname.curselection()[0]
		self.display_attends_entry(attends_list_index)

	def get_attends_list_email(self, event):
		attends_list_index = self.attends_list_email.curselection()[0]
		self.display_attends_entry(attends_list_index)

	# unit saves
	def save_attends_id(self, window):
		attends_list_index = self.attends_id_entry.get()
		db.execute('UPDATE Attendings SET ID=self.attends_id_entry.get() WHERE ID=attends_list_index')
		init_vars
		window.destroy

	def save_attends_fname(self, window):
		attends_list_index = self.attends_id_entry.get()
		Attendings_Table.update(dict(ID=attends_list_index, FNAME=self.attends_fname_entry.get().rstrip()), ['ID'])
		init_vars
		window.destroy

	def save_attends_lname(self, window):
		attends_list_index = self.attends_id_entry.get()
		Attendings_Table.update(dict(ID=attends_list_index, LNAME=self.attends_lname_entry.get().rstrip()), ['ID'])
		init_vars
		window.destroy

	def save_attends_dirname(self, window):
		attends_list_index = self.attends_id_entry.get()
		Attendings_Table.update(dict(ID=attends_list_index, DIRNAME=self.attends_dirname_entry.get().rstrip()), ['ID'])
		init_vars
		window.destroy

	def save_attends_email(self, window):
		attends_list_index = self.attends_id_entry.get()
		Attendings_Table.update(dict(ID=attends_list_index, EMAIL=self.attends_email_entry.get().rstrip()), ['ID'])
		init_vars
		window.destroy

	def set_attendings(self):

		init_vars()
		attends = Toplevel(self.parent)
		attends.wm_title("Jarvs Attendings")
		attends_window = Frame(attends, bg=background_color)
		attends_window.pack(fill=BOTH, expand=True)


		# column labels
		attends_label_id = Label(attends_window, text="ID", bg=background_color, fg=user_color)
		attends_label_id.grid(column=0, row=0, padx=0, pady=0, sticky=W)

		attends_label_fname = Label(attends_window, text="FNAME", bg=background_color, fg=user_color)
		attends_label_fname.grid(column=1, row=0, padx=0, pady=0, sticky=W)

		attends_label_lname = Label(attends_window, text="LNAME", bg=background_color, fg=user_color)
		attends_label_lname.grid(column=2, row=0, padx=0, pady=0, sticky=W)

		attends_label_dirname = Label(attends_window, text="DIRNAME", bg=background_color, fg=user_color)
		attends_label_dirname.grid(column=3, row=0, padx=0, pady=0, sticky=W)

		attends_label_email = Label(attends_window, text="EMAIL", bg=background_color, fg=user_color)
		attends_label_email.grid(column=4, row=0, padx=0, pady=0, sticky=W)

		# data listboxes
		self.attends_list_id = Listbox(attends_window, width=6, height=12, highlightthickness=0, bd=0, selectmode=SINGLE)
		self.attends_list_id.grid(column=0, row=1, padx=0, pady=0)
		self.attends_list_id.bind('<ButtonRelease-1>', self.get_attends_list_id)

		self.attends_list_fname = Listbox(attends_window, width=20, height=12, bd=0, highlightthickness=0, selectmode=SINGLE)
		self.attends_list_fname.grid(column=1, row=1, padx=0, pady=2)
		self.attends_list_fname.bind('<ButtonRelease-1>', self.get_attends_list_fname)

		self.attends_list_lname = Listbox(attends_window, width=16, height=12, bd=0, highlightthickness=0, selectmode=SINGLE)
		self.attends_list_lname.grid(column=2, row=1, padx=0, pady=2)
		self.attends_list_lname.bind('<ButtonRelease-1>', self.get_attends_list_lname)

		self.attends_list_dirname = Listbox(attends_window, width=32, height=12, bd=0, highlightthickness=0, selectmode=SINGLE)
		self.attends_list_dirname.grid(column=3, row=1, padx=0, pady=2)
		self.attends_list_dirname.bind('<ButtonRelease-1>', self.get_attends_list_dirname)


		self.attends_list_email = Listbox(attends_window, width=32, height=12, bd=0, highlightthickness=0, selectmode=SINGLE)
		self.attends_list_email.grid(column=4, row=1, padx=0, pady=2)
		self.attends_list_email.bind('<ButtonRelease-1>', self.get_attends_list_email)

		self.populate_attends_list()

		# entry field

		self.attends_id_entry = Entry(attends_window, width=5, bd=0, highlightthickness=0)
		self.attends_id_entry.grid(column=0, row=2, padx=0, pady=2)

		self.attends_fname_entry = Entry(attends_window, width=19, bd=0, highlightthickness=0)
		self.attends_fname_entry.grid(column=1, row=2, padx=0, pady=2)

		self.attends_lname_entry = Entry(attends_window, width=15, bd=0, highlightthickness=0)
		self.attends_lname_entry.grid(column=2, row=2, padx=0, pady=2)

		self.attends_dirname_entry = Entry(attends_window, width=31, bd=0, highlightthickness=0)
		self.attends_dirname_entry.grid(column=3, row=2, padx=0, pady=2)

		self.attends_email_entry = Entry(attends_window, width=31, bd=0, highlightthickness=0)
		self.attends_email_entry.grid(column=4, row=2, padx=0, pady=2)

		# entry save buttons
		save_id = lambda: self.save_attends_id(attends)
		self.attends_save_id = Button(attends_window, text="Save", width=2, highlightthickness=0, bg=background_color, fg=user_color, bd=0)
		self.attends_save_id.grid(column=0, row=3, padx=0, pady=2)

		save_fname = lambda: self.save_attends_fname(attends)
		self.attends_save_fname = Button(attends_window, text="Save", command=save_fname, width=2, highlightthickness=0, bg=background_color, fg=user_color, bd=0)
		self.attends_save_fname.grid(column=1, row=3, padx=0, pady=2)
		
		save_lname = lambda: self.save_attends_lname(attends)
		self.attends_save_lname = Button(attends_window, text="Save", command=save_lname, width=2, highlightthickness=0, bg=background_color, fg=user_color, bd=0)
		self.attends_save_lname.grid(column=2, row=3, padx=0, pady=2)

		save_dirname = lambda: self.save_attends_dirname(attends)
		self.attends_save_dirname = Button(attends_window, text="Save", command=save_dirname, width=2, highlightthickness=0, bg=background_color, fg=user_color, bd=0)
		self.attends_save_dirname.grid(column=3, row=3, padx=0, pady=2)

		save_email = lambda: self.save_attends_email(attends)
		self.attends_save_email = Button(attends_window, text="Save", command=save_email, width=2, highlightthickness=0, bg=background_color, fg=user_color, bd=0)
		self.attends_save_email.grid(column=4, row=3, padx=0, pady=2)

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

	def test_email(self):
		root_dir = os.getcwd()
		os.chdir("../..")
		subprocess.Popen(["./RVS_test_emailer.sh"], shell=True)

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
	global db
	db = dataset.connect('sqlite:///rvs/RVS.db')
	global Preferences_Table
	Preferences_Table = db['Preferences']
	global Attendings_Table
	Attendings_Table = db['Attendings']

	Preferences_Data = Preferences_Table.find_one(ID=0)
	global user_name
	user_name = Preferences_Data.get('USERNAME')
	global user_email
	user_email = Preferences_Data.get("USEREMAIL")
	global user_color
	user_color = Preferences_Data.get("USERCOLOR")
	global jarvs_color
	jarvs_color = Preferences_Data.get("JARVSCOLOR")
	global background_color
	background_color = Preferences_Data.get("BACKGROUNDCOLOR")

	global attending_ids
	attending_ids = []
	Attending_IDs_raw = db.query('SELECT ID FROM Attendings')
	for Row in Attending_IDs_raw:
		attending_ids.append(Row['ID'])

def main():
	root = Tk()
	app = Jarvs(root)
	root.mainloop()

# conditionally execute script or as module if imported elsewhere
if __name__ == '__main__':
	init_vars()
	main()
