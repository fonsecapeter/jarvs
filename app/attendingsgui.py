#!/usr/bin/env python
# import standard & 3rd party libraries
from Tkinter import *
import tkMessageBox
# import jarvs-specific methods
##import rvsdata
##import practice_rvsdata {IN __init__}

class Attendings(Frame):

	def __init__(self, parent, database):
		Frame.__init__(self, parent)

		self.database = database

		global rvsdata
		if self.database == "practice":
			import rvspracticedata as rvsdata  
		else:
			import rvsdata

		self.parent = parent
		self.init_ui()

	def init_ui(self):
		self.attends = Frame(self.parent, bg=gray_color)
		self.parent.title("Attendings")
		self.attends.pack(fill=BOTH, expand=True)
		##attends.wm_title("Jarvs Attendings")
		attends_window = Frame(self.attends, bg=gray_color, bd=0)
		attends_window.grid(row=0, column=2, sticky=N)
		attends_right = Frame(self.attends, bg=gray_color, bd=0)
		attends_right.grid(row=0, column=0, rowspan=2)
		attends_separator = Frame(self.attends, bd=1, width=2)
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
		save_attends = lambda: self.save_attends(self.attends)
		self.attends_save_all = Button(attends_right,text="Save", command=save_attends, bg="white", bd=0)
		self.attends_save_all.grid(column=0, row=6, padx=0, pady=12)

		# entry delete button
		delete_attends = lambda: self.delete_attends(self.attends)
		self.attends_delete_button = Button(attends_right, text="Delete", command=delete_attends, bg="white", bd=0)
		self.attends_delete_button.grid(column=0, row=7, padx=0, pady=2)

	# <--- edit and display attendings data --->
	def populate_attends_list(self):
		for Attending_ID in range(rvsdata.attending_ids[-1] + 1):
			try:
				self.attends_list_fname.insert(rvsdata.attending_ids[Attending_ID], rvsdata.attending_fnames[Attending_ID])
			except:
				pass

		self.attends_list_fname.insert(END, "+")



		# colorize alternating rows
		for Row in range(1, len(rvsdata.attending_ids), 2):
			self.attends_list_fname.itemconfigure(Row, background=dark_gray_color)

	# populate attending entry from fname listbox
	def populate_attends_entry(self, event):
		attends_list_index = self.attends_list_fname.curselection()[0]

		if attends_list_index < len(rvsdata.attending_ids):
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

	def save_attends(self, window):
		current_attending_id = int(self.attends_id_entry.get())
		new_attending_fname = self.attends_fname_entry.get()
		new_attending_lname = self.attends_lname_entry.get()
		new_attending_dirname = self.attends_dirname_entry.get()
		new_attending_email = self.attends_email_entry.get()
		# update existing row in db if editting existing attending
		# ASSUMPTION: attending_id's sorted and greatest integer value id is at last position of array
		# TODO: sort in rvsdata to ensure this
		if current_attending_id <= rvsdata.attending_ids[-1]:
			rvsdata.update_attending_fname(new_attending_fname, current_attending_id)
			rvsdata.update_attending_lname(new_attending_lname, current_attending_id)
			rvsdata.update_attending_dirname(new_attending_dirname, current_attending_id)
			rvsdata.update_attending_email(new_attending_email, current_attending_id)
		else:
			rvsdata.insert_new_attending(new_attending_fname, new_attending_lname, new_attending_dirname, new_attending_email)
		reload(rvsdata)
		init_vars()
		self.update()
		self.attends.pack_forget()
		self.init_ui()

	def delete_attends(self, window):
		current_attending_id = self.attends_id_entry.get()

		# warning messages
		if tkMessageBox.askyesno("Verify", "Permanently delete my memory of attending #"+current_attending_id+"?"):
			tkMessageBox.showwarning("Yes", "Deleted atteninding #"+current_attending_id)
			rvsdata.delete_attending(current_attending_id)
		else:
			tkMessageBox.showinfo('No', "Deletion has been cancelled")

		reload(rvsdata)
		init_vars()
		self.attends.pack_forget()
		self.init_ui()

def init_vars():
	##reload(rvsdata)

	global gray_color
	gray_color = '#eeeeee'
	global dark_gray_color
	dark_gray_color = '#e6e6e6'

def main(data = "real"):
	# slick hack: import over database translating script
	# to read from practice database vs real database
	init_vars()
	root = Tk()
	if data == "practice":
		app = Attendings(root, "practice")
	else:
		app = Attendings(root, "real")
	root.mainloop()

# conditionally execute script or as module if imported elsewhere
if __name__ == '__main__':
	init_vars()
	main()
