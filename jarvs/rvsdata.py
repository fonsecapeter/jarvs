#!/usr/bin/env python
import sqlite3 as sql


connection = sql.connect('./jarvs/RVS.db')
c = connection.cursor()

#-----------------------------------------------------------------------------------------------
## READ DATA FROM DATABASE
# Attendings  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

attending_ids = []
for Row in c.execute('SELECT id FROM Attendings'):
	attending_ids += Row

attending_fnames = []
for Row in c.execute('SELECT fname FROM Attendings'):
	attending_fnames += Row

attending_lnames = []
for Row in c.execute('SELECT lname FROM Attendings'):
	attending_lnames += Row

attending_dirnames = []
for Row in c.execute('SELECT DIRNAME FROM Attendings'):
	attending_dirnames += Row

attending_emails = []
for Row in c.execute('SELECT email FROM Attendings'):
	attending_emails += Row

# Preferences  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

user_ids = []
for Row in c.execute('SELECT id FROM Preferences'):
	user_ids = Row

user_names = []
for Row in c.execute('SELECT username FROM Preferences'):
	user_names = Row

user_emails = []
for Row in c.execute('SELECT useremail FROM Preferences'):
	user_emails = Row

user_colors = []
for Row in c.execute('SELECT usercolor FROM Preferences'):
	user_colors = Row

jarvs_colors = []
for Row in c.execute('SELECT jarvscolor FROM Preferences'):
	jarvs_colors = Row

background_colors = []
for Row in c.execute('SELECT backgroundcolor FROM Preferences'):
	background_colors = Row

root_dirs = []
for Row in c.execute('SELECT rootdir From Preferences'):
	root_dirs = Row

# only one row, still need to pip data from db > array > int/string
user_id = user_ids[0]
user_name = user_names[0]
user_email = user_emails[0]
user_color = user_colors[0]
jarvs_color = jarvs_colors[0]
background_color = background_colors[0]
root_dir = root_dirs[0]

#-----------------------------------------------------------------------------------------------
## UPDATE DATA IN DATABASE
# ATTENDINGS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def update_attending_id(new_id, old_id):
	connection.execute('UPDATE Attendings SET id=? WHERE id=?', (new_id, old_id))
	connection.commit()

def update_attending_fname(new_fname, attending_id):
	connection.execute('UPDATE Attendings SET fname=? WHERE id=?', (new_fname, attending_id))
	connection.commit()

def update_attending_lname(new_lname, attending_id):
	connection.execute('UPDATE Attendings SET lname=? WHERE id=?', (new_lname, attending_id))
	connection.commit()

def update_attending_dirname(new_dirname, attending_id):
	connection.execute('UPDATE Attendings SET DIRNAME=? WHERE id=?', (new_dirname, attending_id))
	connection.commit()

def update_attending_email(new_email, attending_id):
	connection.execute('UPDATE Attendings SET email=? WHERE id=?', (new_email, attending_id))
	connection.commit()

# Preferences   -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def update_user_id(new_id, old_id):
	connection.execute('UPDATE Preferences SET id=? WHERE id=?', (new_id, old_id))
	connection.commit()

def update_user_name(new_user_name):
	connection.execute('UPDATE Preferences SET username=? WHERE id=0', (new_user_name,))
	connection.commit()

def update_user_email(new_user_email):
	connection.execute('UPDATE Preferences SET useremail=? WHERE id=0', (new_user_email,))
	connection.commit()

def update_user_color(new_user_color):
	connection.execute('UPDATE Preferences SET usercolor=? WHERE id=0', (new_user_color,))
	connection.commit()

def update_jarvs_color(new_jarvs_color):
	connection.execute('UPDATE Preferences SET jarvscolor=? WHERE id=0', (new_jarvs_color,))
	connection.commit()

def update_background_color(new_background_color):
	connection.execute('UPDATE Preferences SET backgroundcolor=? WHERE id=0', (new_background_color,))
	connection.commit()

def update_root_dir(new_root_dir):
	connection.execute('UPDATE Preferences SET rootdir=? WHERE id=0', (new_root_dir,))
	connection.commit()

#-----------------------------------------------------------------------------------------------
## CREATE DATA IN DATABASE
# ATTENDINGS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def insert_new_attending(new_fname, new_lname, new_dirname, new_email):
	new_id = attending_ids[-1] + 1
	connection.execute('INSERT INTO Attendings VALUES (?, ?, ?, ?, ?)', (new_id, new_fname, new_lname, new_dirname, new_email))
	connection.commit()

#-----------------------------------------------------------------------------------------------
## DELETE DATA IN DATABASE
# ATTENDINGS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def delete_attending(attending_id):
	connection.execute('DELETE FROM Attendings WHERE id=?', (attending_id,))
	connection.commit()
