#!/usr/bin/env python
# import 3rd party libraries
from Tkinter import *
import tkMessageBox
import os
import subprocess
import time
import sqlite3 as sql
from PIL import Image, ImageTk
# import jarvs-specific methods
import rvsdata
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
		form = Frame(self.parent, bg=rvsdata.background_color, bd=0)
		form.pack(fill=BOTH, expand=True)

		self.input_content = StringVar()
		self.entry_main = Entry(form, fg=rvsdata.user_color, bg=rvsdata.background_color, insertbackground=rvsdata.user_color, highlightthickness=0, bd=0)
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
		prefs_window = Frame(prefs, bg=gray_color)
		prefs_window.pack(fill=BOTH, expand=True)

		# user_name
		self.user_name_label = Label(prefs_window, text="User Name: ", bg=gray_color)
		self.user_name_label.grid(row=0, column=0, sticky=E, padx=2, pady=2)
		self.user_name_entry = Entry(prefs_window, bd=0)
		self.user_name_entry.insert(END, rvsdata.user_name)
		self.user_name_entry.grid(row=0, column=1, padx=2, pady=2)
		self.user_name_entry.bind('<Return>', self.save_user_name)

		# email
		self.user_email_label = Label(prefs_window, text="User Email: ", bg=gray_color)
		self.user_email_label.grid(row=1, column=0, sticky=E, padx=2, pady=2)
		self.user_email_entry = Entry(prefs_window, bd=0)
		self.user_email_entry.insert(END, rvsdata.user_email)
		self.user_email_entry.grid(row=1, column=1, padx=2, pady=2)
		self.user_email_entry.bind('<Return>', self.save_user_email)

		# color
		self.user_color_label = Label(prefs_window, text="User Color: ", bg=gray_color)
		self.user_color_label.grid(row=2, column=0, sticky=E, padx=2, pady=2)
		self.user_color_entry = Entry(prefs_window, bd=0)
		self.user_color_entry.insert(END, rvsdata.user_color)
		self.user_color_entry.grid(row=2, column=1, padx=2, pady=2)
		self.user_color_entry.bind('<Return>', self.save_user_color)

		self.jarvs_color_label = Label(prefs_window, text="Jarvs Color: ", bg=gray_color)
		self.jarvs_color_label.grid(row=3, column=0, sticky=E, padx=2, pady=2)
		self.jarvs_color_entry = Entry(prefs_window, bd=0)
		self.jarvs_color_entry.insert(END, rvsdata.jarvs_color)
		self.jarvs_color_entry.grid(row=3, column=1, padx=2, pady=2)
		self.jarvs_color_entry.bind('<Return>', self.save_jarvs_color)

		self.background_color_label = Label(prefs_window, text="Background Color: ", bg=gray_color)
		self.background_color_label.grid(row=4, column=0, sticky=E, padx=2, pady=2)
		self.background_color_entry = Entry(prefs_window, bd=0)
		self.background_color_entry.insert(END, rvsdata.background_color)
		self.background_color_entry.grid(row=4, column=1, padx=2, pady=2)
		self.background_color_entry.bind('<Return>', self.save_background_color)

		self.color_label = Label(prefs_window, text="( enter color as name or hex )", bg=gray_color)
		self.color_label.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

		# save all button
		self.save_prefs_button = Button(prefs_window, text="Save", bg="white", bd=0)
		self.save_prefs_button.bind('<Button-1>', self.save_all_preferences)
		self.save_prefs_button.grid(row=6, column=0, columnspan=2, padx=2, pady=2)

	# unit saves
	def save_user_name(self, event):
		rvsdata.update_user_name(self.user_name_entry.get().rstrip(), 0)

	def save_user_email(self, event):
		rvsdata.update_user_color(self.user_email_entry.get().rstrip(), 0)

	def save_user_color(self, event):
		rvsdata.update_user_color(self.user_color_entry.get().rstrip(), 0)

	def save_jarvs_color(self, event):
		rvsdata.update_jarvs_color(self.jarvs_color_entry.get().rstrip(), 0)

	def save_background_color(self, event):
		rvsdata.update_background_color(self.background_color_entry.get().rstrip(), 0)

	# save all
	def save_all_preferences(self, event):
		self.save_user_name(event)
		self.save_user_email(event)
		self.save_user_color(event)
		self.save_jarvs_color(event)
		self.save_background_color(event)
		init_vars()
		self.text_content.configure(fg=rvsdata.jarvs_color, bg=rvsdata.background_color)
		self.text_content.tag_configure('user', foreground=rvsdata.user_color)
		self.update()

	# <--- edit and display attendings data --->
	def populate_attends_list(self):
		for Attending in rvsdata.attending_ids:
			self.attends_list_fname.insert(Attending, rvsdata.attending_fnames[Attending])

		self.attends_list_fname.insert(END, "+")



		# colorize alternating rows
		for Row in range(1, len(rvsdata.attending_ids), 2):
			self.attends_list_fname.itemconfigure(Row, background=dark_gray_color)

	# populate attending entry from fname listbox
	def populate_attends_entry(self, event):
		attends_list_index = self.attends_list_fname.curselection()[0]

		if attends_list_index < rvsdata.attending_ids[-1] + 1:
			self.attends_id_entry.config(state=NORMAL)
			self.attends_id_entry.delete(0, END)
			self.attends_id_entry.insert(END, rvsdata.attending_ids[attends_list_index])
			self.attends_id_entry.config(state=DISABLED)

			self.attends_fname_entry.delete(0, END)
			self.attends_fname_entry.insert(END, rvsdata.attending_fnames[attends_list_index])

			self.attends_lname_entry.delete(0, END)
			self.attends_lname_entry.insert(END, rvsdata.attending_lnames[attends_list_index])

			self.attends_dirname_entry.delete(0, END)
			self.attends_dirname_entry.insert(END, rvsdata.attending_dirnames[attends_list_index])

			self.attends_email_entry.delete(0, END)
			self.attends_email_entry.insert(END, rvsdata.attending_emails[attends_list_index])
		else:
			self.attends_id_entry.config(state=NORMAL)
			self.attends_id_entry.delete(0, END)
			self.attends_id_entry.insert(END, rvsdata.attending_ids[-1] + 1)
			self.attends_id_entry.config(state=DISABLED)

			self.attends_fname_entry.delete(0, END)
			self.attends_fname_entry.insert(END, "New First Name")

			self.attends_lname_entry.delete(0, END)
			self.attends_lname_entry.insert(END, "New Last Name")

			self.attends_dirname_entry.delete(0, END)
			self.attends_dirname_entry.insert(END, "New Directory Name")

			self.attends_email_entry.delete(0, END)
			self.attends_email_entry.insert(END, "New Email")


	# unit saves
	def save_attends_fname(self, current_attending_id):
		new_attending_fname = self.attends_fname_entry.get()
		rvsdata.update_attending_fname(new_attending_fname, current_attending_id)

	def save_attends_lname(self, current_attending_id):
		new_attending_lname = self.attends_lname_entry.get()
		rvsdata.update_attending_lname(new_attending_lname, current_attending_id)

	def save_attends_dirname(self, current_attending_id):
		new_attending_dirname = self.attends_dirname_entry.get()
		rvsdata.update_attending_dirname(new_attending_dirname, current_attending_id)

	def save_attends_email(self, current_attending_id):
		new_attending_email = self.attends_email_entry.get()
		rvsdata.update_attending_email(new_attending_email, current_attending_id)

	def save_attends(self, window):
		current_attending_id = self.attends_id_entry.get()
		new_attending_fname = self.attends_fname_entry.get()
		new_attending_lname = self.attends_lname_entry.get()
		new_attending_dirname = self.attends_dirname_entry.get()
		new_attending_email = self.attends_email_entry.get()
		if current_attending_id < rvsdata.attending_ids[-1] + 1:
			self.save_attends_fname(current_attending_id)
			self.save_attends_lname(current_attending_id)
			self.save_attends_dirname(current_attending_id)
			self.save_attends_email(current_attending_id)
		else:
			rvsdata.insert_new_attending(new_attending_fname, new_attending_lname, new_attending_dirname, new_attending_email)
		init_vars()
		window.destroy()
		self.set_attendings()

	def delete_attends(self, window):
		current_attending_id = self.attends_id_entry.get()
		rvsdata.delete_attending(current_attending_id)
		init_vars()
		window.destroy()
		self.set_attendings()

	def set_attendings(self):

		init_vars()
		attends = Toplevel(self.parent, bg=gray_color)
		attends.wm_title("Jarvs Attendings")
		attends_window = Frame(attends, bg=gray_color, bd=0)
		attends_window.grid(row=0, column=2, sticky=N)
		attends_right = Frame(attends, bg=gray_color, bd=0)
		attends_right.grid(row=0, column=0, rowspan=2)
		attends_separator = Frame(attends, bd=1, width=2)
		attends_separator.grid(row=0, column=1, sticky=N+S)

		# data listbox
		self.attends_list_fname_scroll = Scrollbar(attends_window, bd=0, troughcolor=rvsdata.user_color, highlightthickness=0)
		##self.attends_list_fname_scroll.grid(column=2, row=0, padx=0, pady=0, sticky=W+N+S)
		self.attends_list_fname = Listbox(attends_window, width=20, height=20, bd=0, highlightthickness=0, yscrollcommand=self.attends_list_fname_scroll.set, selectmode=SINGLE)
		self.attends_list_fname.grid(column=1, row=0, padx=0, pady=2, sticky=W+N)
		self.attends_list_fname.bind('<ButtonRelease-1>', self.populate_attends_entry)
		self.attends_list_fname_scroll.config(command=self.attends_list_fname.yview)

		self.populate_attends_list()

		# entry fields
		#self.attends_photo = ImageTk.PhotoImage(attending_image)
		#self.attends_icon = Label(attends_right, image=self.attends_photo, bg=gray_color)
		#self.attends_icon.image = self.attends_photo
		#self.attends_icon.grid(column=0, row=0, padx=2, pady=12)

		self.attends_id_entry = Entry(attends_right, bd=0, bg=gray_color, disabledbackground=gray_color, width=32, highlightthickness=0, justify=CENTER, state=NORMAL)
		self.attends_id_entry.grid(column=0, row=1, padx=0, pady=2)
		self.attends_id_entry.insert(0, "-- ID --")
		self.attends_id_entry.config(state=DISABLED)

		self.attends_fname_entry = Entry(attends_right, bd=0, bg=gray_color, width=32, highlightthickness=0, justify=CENTER)
		self.attends_fname_entry.grid(column=0, row=2, padx=0, pady=2)
		self.attends_fname_entry.insert(0, "-- First Name --")

		self.attends_lname_entry = Entry(attends_right, bd=0, bg=gray_color, width=32, highlightthickness=0, justify=CENTER)
		self.attends_lname_entry.grid(column=0, row=3, padx=0, pady=2)
		self.attends_lname_entry.insert(0, "-- Last Name --")

		self.attends_dirname_entry = Entry(attends_right, bd=0, bg=gray_color, width=32, highlightthickness=0, justify=CENTER)
		self.attends_dirname_entry.grid(column=0, row=4, padx=0, pady=2)
		self.attends_dirname_entry.insert(0, "-- Directory Name --")

		self.attends_email_entry = Entry(attends_right, bd=0, bg=gray_color, width=32, highlightthickness=0, justify=CENTER)
		self.attends_email_entry.grid(column=0, row=5, padx=0, pady=2)
		self.attends_email_entry.insert(0, "-- Email --")

		# entry save button
		save_attends = lambda: self.save_attends(attends)
		self.attends_save_all = Button(attends_right,text="Save", command=save_attends, bg="white", bd=0)
		self.attends_save_all.grid(column=0, row=6, padx=0, pady=12)

		# entry delete button
		delete_attends = lambda: self.delete_attends(attends)
		self.attends_delete_button = Button(attends_right, text="Delete", command=delete_attends, bg="white", bd=0)
		self.attends_delete_button.grid(column=0, row=7, padx=0, pady=2)

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
	reload(rvsdata)

	global gray_color
	gray_color = '#eeeeee'
	global dark_gray_color
	dark_gray_color = '#e6e6e6'

	#global attending_image
	#attending_image = Image.open("design/attending_icon.png")
	#attending_image = attending_image.resize((98, 98), Image.ANTIALIAS)

def main():
	root = Tk()
	app = Jarvs(root)
	root.mainloop()

# conditionally execute script or as module if imported elsewhere
if __name__ == '__main__':
	init_vars()
	main()
