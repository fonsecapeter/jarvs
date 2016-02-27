#!/usr/bin/env python
import sqlite3 as sql


connection = sql.connect('rvs/RVS.db')
c = connection.cursor()

#-----------------------------------------------------------------------------------------------
## READ DATA FROM DATABASE
# Attendings  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

attending_ids = []
for Row in c.execute('SELECT ID FROM Attendings'):
	attending_ids += Row

attending_fnames = []
for Row in c.execute('SELECT FNAME FROM Attendings'):
	attending_fnames += Row

attending_lnames = []
for Row in c.execute('SELECT LNAME FROM Attendings'):
	attending_lnames += Row

attending_dirnames = []
for Row in c.execute('SELECT DIRNAME FROM Attendings'):
	attending_dirnames += Row

attending_emails = []
for Row in c.execute('SELECT EMAIL FROM Attendings'):
	attending_emails += Row

# Preferences  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

user_ids = []
for Row in c.execute('SELECT ID FROM Preferences'):
	user_ids = Row

user_names = []
for Row in c.execute('SELECT USERNAME FROM Preferences'):
	user_names = Row

user_emails = []
for Row in c.execute('SELECT USEREMAIL FROM Preferences'):
	user_emails = Row

user_colors = []
for Row in c.execute('SELECT USERCOLOR FROM Preferences'):
	user_colors = Row

jarvs_colors = []
for Row in c.execute('SELECT JARVSCOLOR FROM Preferences'):
	jarvs_colors = Row

background_colors = []
for Row in c.execute('SELECT BACKGROUNDCOLOR FROM Preferences'):
	background_colors = Row

user_id = user_ids[0]
user_name = user_names[0]
user_email = user_emails[0]
user_color = user_colors[0]
jarvs_color = jarvs_colors[0]
background_color = background_colors[0]

#-----------------------------------------------------------------------------------------------
## UPDATE DATA IN DATABASE
# ATTENDINGS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def update_attending_id(new_id, old_id):
	connection.execute('UPDATE Attendings SET ID=? WHERE ID=?', (new_id, old_id))
	connection.commit()

def update_attending_fname(new_fname, attending_id):
	connection.execute('UPDATE Attendings SET FNAME=? WHERE ID=?', (new_fname, attending_id))
	connection.commit()

def update_attending_lname(new_lname, attending_id):
	connection.execute('UPDATE Attendings SET LNAME=? WHERE ID=?', (new_lname, attending_id))
	connection.commit()

def update_attending_dirname(new_dirname, attending_id):
	connection.execute('UPDATE Attendings SET DIRNAME=? WHERE ID=?', (new_dirname, attending_id))
	connection.commit()

def update_attending_email(new_email, attending_id):
	connection.execute('UPDATE Attendings SET EMAIL=? WHERE ID=?', (new_email, attending_id))
	connection.commit()

# Preferences   -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def update_user_id(new_id, old_id):
	connection.execute('UPDATE Preferencess SET ID=? WHERE ID=?', (new_id, old_id))
	connection.commit()

def update_user_name(new_user_name, user_id):
	connection.execute('UPDATE Preferencess SET USERNAME=? WHERE ID=?', (new_user_name, user_id))
	connection.commit()

def update_user_email(new_user_email, user_id):
	connection.execute('UPDATE Preferencess SET USEREMAIL=? WHERE ID=?', (new_user_email, user_id))
	connection.commit()

def update_user_color(new_user_color, user_id):
	connection.execute('UPDATE Preferencess SET USERCOLOR=? WHERE ID=?', (new_user_color, user_id))
	connection.commit()

def update_jarvs_color(new_jarvs_color, user_id):
	connection.execute('UPDATE Preferencess SET JARVSCOLOR=? WHERE ID=?', (new_jarvs_color, user_id))
	connection.commit()

def update_background_color(new_background_color, user_id):
	connection.execute('UPDATE Preferencess SET BACKGROUNDCOLOR=? WHERE ID=?', (new_background_color, user_id))
	connection.commit()

#-----------------------------------------------------------------------------------------------
## CREATE DATA IN DATABASE
# ATTENDINGS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def insert_new_attending(new_fname, new_lname, new_dirname, new_email):
	new_id = attending_ids[-1] + 1
	print new_id
	connection.execute('INSERT INTO Attendings VALUES (?, ?, ?, ?, ?)', (new_id, new_fname, new_lname, new_dirname, new_email))
	connection.commit()

#-----------------------------------------------------------------------------------------------
## DELETE DATA IN DATABASE
# ATTENDINGS  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

def delete_attending(attending_id):
	connection.execute('DELETE FROM Attendings WHERE ID=?', attending_id)
	connection.commit()
