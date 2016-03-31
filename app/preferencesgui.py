#!/usr/bin/env python
# import standard & 3rd party libraries
from Tkinter import *
import tkColorChooser
# import jarvs-specific methods
import rvspracticedata as rvsdata

##class Preferences(Frame):
class Preferences(Toplevel):
	# class variables
	gray_color = '#eeeeee'
	##Frame = Frame

	def __init__(self, parent):
		self.parent = parent
		self.init_ui()

	def init_ui(self):
		self.prefs = Toplevel(self.parent)
		##self.prefs = Frame(self.parent, bg=Preferences.gray_color)
		##self.parent.title("Preferences")
		self.prefs.title("Preferences")
		##self.prefs.pack(fill=BOTH, expand=True)
		self.prefs_window = Frame(self.prefs, bg=Preferences.gray_color)
		self.prefs_window.pack(fill=BOTH, expand=True)

		# user_name
		self.user_name_label = Label(self.prefs_window, text="User Name: ", bg=Preferences.gray_color)
		self.user_name_label.grid(row=0, column=0, sticky=E, padx=2, pady=2)
		self.user_name_entry = Entry(self.prefs_window, bd=0, width=32)
		self.user_name_entry.insert(END, rvsdata.user_name)
		self.user_name_entry.grid(row=0, column=1, padx=2, pady=2)
		##self.user_name_entry.bind('<Return>', self.save_user_name)

		# email
		self.user_email_label = Label(self.prefs_window, text="User Email: ", bg=Preferences.gray_color)
		self.user_email_label.grid(row=1, column=0, sticky=E, padx=2, pady=2)
		self.user_email_entry = Entry(self.prefs_window, bd=0, width=32)
		self.user_email_entry.insert(END, rvsdata.user_email)
		self.user_email_entry.grid(row=1, column=1, padx=2, pady=2)
		##self.user_email_entry.bind('<Return>', self.save_user_email)

		# color
		self.user_color_label = Label(self.prefs_window, text="User Color: ", bg=Preferences.gray_color)
		self.user_color_label.grid(row=2, column=0, sticky=E, padx=2, pady=2)
		self.user_color_entry = Entry(self.prefs_window, bd=0, width=32)
		self.user_color_entry.insert(END, rvsdata.user_color)
		self.user_color_entry.grid(row=2, column=1, padx=2, pady=2)
		##self.user_color_entry.bind('<Return>', self.save_user_color)
		self.user_color_selector = Button(self.prefs_window, text="Color Picker", bg="white", bd=0, command=lambda: self.select_color("user_color"))
		self.user_color_selector.grid(row=2, column=2, padx=2, pady=2)

		self.jarvs_color_label = Label(self.prefs_window, text="Jarvs Color: ", bg=Preferences.gray_color)
		self.jarvs_color_label.grid(row=3, column=0, sticky=E, padx=2, pady=2)
		self.jarvs_color_entry = Entry(self.prefs_window, bd=0, width=32)
		self.jarvs_color_entry.insert(END, rvsdata.jarvs_color)
		self.jarvs_color_entry.grid(row=3, column=1, padx=2, pady=2)
		##self.jarvs_color_entry.bind('<Return>', self.save_jarvs_color)
		self.jarvs_color_selector = Button(self.prefs_window, text="Color Picker", bg="white", bd=0, command=lambda: self.select_color("jarvs_color"))
		self.jarvs_color_selector.grid(row=3, column=2, padx=2, pady=2)

		self.background_color_label = Label(self.prefs_window, text="Background Color: ", bg=Preferences.gray_color)
		self.background_color_label.grid(row=4, column=0, sticky=E, padx=2, pady=2)
		self.background_color_entry = Entry(self.prefs_window, bd=0, width=32)
		self.background_color_entry.insert(END, rvsdata.background_color)
		self.background_color_entry.grid(row=4, column=1, padx=2, pady=2)
		##self.background_color_entry.bind('<Return>', self.save_background_color)
		self.background_color_selector = Button(self.prefs_window, text="Color Picker", bg="white", bd=0, command=lambda: self.select_color("background_color"))
		self.background_color_selector.grid(row=4, column=2, padx=2, pady=2)

		self.color_label = Label(self.prefs_window, text="( enter color as name or hex )", bg=Preferences.gray_color)
		self.color_label.grid(row=5, column=0, columnspan=2, padx=2, pady=2)

		self.root_dir_label = Label(self.prefs_window, text="RVS Root Directory: ", bg=Preferences.gray_color)
		self.root_dir_label.grid(row=6, column=0, sticky=E, padx=2, pady=2)
		self.root_dir_entry = Entry(self.prefs_window, bd=0, width=32)
		self.root_dir_entry.insert(END, rvsdata.root_dir)
		self.root_dir_entry.grid(row=6, column=1, padx=2, pady=2)
		##self.root_dir_entry.bind('<Return>', self.save_root_dir)

		# save all button
		self.save_prefs_button = Button(self.prefs_window, text="Save", bg="white", bd=0)
		self.save_prefs_button.bind('<Button-1>', self.save_all_preferences)
		self.save_prefs_button.grid(row=7, column=0, columnspan=2, padx=2, pady=2)

	# <--- save all --->
	def save_all_preferences(self, event):
		rvsdata.update_user_name(self.user_name_entry.get().rstrip())
		rvsdata.update_user_color(self.user_email_entry.get().rstrip())
		rvsdata.update_user_color(self.user_color_entry.get().rstrip())
		rvsdata.update_jarvs_color(self.jarvs_color_entry.get().rstrip())
		rvsdata.update_background_color(self.background_color_entry.get().rstrip())
		rvsdata.update_root_dir(self.root_dir_entry.get().rstrip())

		reload(rvsdata)
		self.parent.text_content.configure(fg=rvsdata.jarvs_color, bg=rvsdata.background_color)
		self.parent.text_content.tag_configure('user', foreground=rvsdata.user_color)
		self.parent.entry_main.configure(bg=rvsdata.background_color)
		self.parent.form.configure(bg=rvsdata.background_color)
		self.parent.update()
		self.prefs.destroy()
		self.init_ui()

	# <--- color selector popout --->
	def select_color(self, color_type):
		# tkColorChooser outputs tuple, where second is hex, ie new_color[1]
		# outputs (None, None) if cancelled or closed - if all(new_color) checks for None in the tuple
		if color_type == "user_color":
			new_color = tkColorChooser.askcolor(initialcolor=self.user_color_entry.get().rstrip())
			if all(new_color):
				self.user_color_entry.delete(0, 'end')
				self.user_color_entry.insert(0, new_color[1])
		elif color_type == "jarvs_color":
			new_color = tkColorChooser.askcolor(initialcolor=self.jarvs_color_entry.get().rstrip())
			if all(new_color):
				self.jarvs_color_entry.delete(0, 'end')
				self.jarvs_color_entry.insert(0, new_color[1])
		elif color_type == "background_color":
			new_color = tkColorChooser.askcolor(initialcolor=self.background_color_entry.get().rstrip())
			if all(new_color):
				self.background_color_entry.delete(0, 'end')
				self.background_color_entry.insert(0, new_color[1])

def main(parent):
	prefs_app = Preferences(parent)

if __name__ == '__main__':
	main()