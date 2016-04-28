#!/usr/bin/env python
# build the user's $HOME/.jarvs/ directory containing shell scripts and user-level data
### BEGIN LICENSE
# Copyright (C) 2016 Peter <pfonseca@mac-cloud-vm-163-239.ucsf.edu>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import os
import sqlite3
import shellscripts
home = os.path.expanduser("~")
home_jarvs = home + "/.jarvs"

def build(scripts):
	# make ~/.jarvs
	print "checking " + home_jarvs + "..."
	try:
		os.makedirs(home_jarvs)
	except OSError as exception:
		if not os.path.isdir(home_jarvs):
			raise
 	# create database
	print "checking database..."
	conn = sqlite3.connect(home_jarvs + "/RVS.db")
	print "checking preferences table..."
	conn.execute("""
			CREATE TABLE IF NOT EXISTS Preferences (
			id   INT PRIMARY KEY   NOT NULL,
			username        TEXT   NOT NULL,
			useremail       TEXT   NOT NULL,
			usercolor       TEXT   NOT NULL,
			jarvscolor      TEXT   NOT NULL,
			backgroundcolor TEXT   NOT NULL,
			rootdir         TEXT   NOT NULL);""")
	conn.commit()

	try:
		conn.execute('INSERT INTO Preferences VALUES (0, "Peter", "peter.nfonseca@gmail.com", "#e6e6e6", "#e29d36", "#2c303e", "/home/peter/jarvs/app/rvs/Outstanding/");')
		conn.commit()
		print "initializing preferences..."
	except:		
		pass

	print "checking attendings table..."
	conn.execute("""
			CREATE TABLE IF NOT EXISTS Attendings (
			id   INT PRIMARY KEY   NOT NULL,
			fname           TEXT   NOT NULL,
			lname           TEXT   NOT NULL,
			dirname         TEXT   NOT NULL,
			email           TEXT   NOT NULL);""")
	conn.commit()

	try:
		conn.execute('INSERT INTO Attendings VALUES ( 0, "Elaine",    "Benes",    "Benes,Elaine/",    "elaine.benes@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 1, "George",    "Costanza", "Costanza,George/", "george.costanza@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 2, "Julius",    "Hibbert",  "Hibbert,Julius/",  "julius.hibbert@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 3, "Clark",     "Kent",     "Kent,Clark/",      "super.man@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 4, "Cosmo",     "Kramer",   "Kramer,Cosmo/",    "cosmo@gmail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 5, "Elizabeth", "Lemon",    "Lemon,Elizabeth/", "the.lizard@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 6, "Lex",       "Luthor",   "Luthor,Lex/",      "kryptonite@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 7, "Nick",      "Riviera",  "Riviera,Nick/",    "nick.riviera@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 8, "Jerry",     "Seinfeld", "Seinfeld,Jerry/",  "jerry.seinfeld@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES ( 9, "Neil",      "Spaceman", "Spaceman,Neil/",   "dr.spaceman@fakemail.com");')
		conn.execute('INSERT INTO Attendings VALUES (10, "Bob",       "Vance",    "Vance,Bob/",       "bob.vance@vancerefridgeration.com");')
		conn.execute('INSERT INTO Attendings VALUES (11, "Art",       "Vandalay", "Vandalay,Art/",    "art.vandalay@vandalayarchitecture.com");')
		conn.commit()
		print "initializing attendings..."
	except:
		pass

	conn.close()

	# build bash shell scripts in ./jarvs
	if not os.path.isfile(home_jarvs + "/RVS_emailer.sh"):
		print "writing RVS_emailer.sh..."
		os.system("touch ${HOME}/.jarvs/RVS_emailer.sh")
		for line in scripts.rvs_emailer:
			command = "echo '" + line + "' | cat >> ${HOME}/.jarvs/RVS_emailer.sh"
			os.system(command)


	if not os.path.isfile(home_jarvs + "/RVS_test_emailer.sh"):
		print "writing RVS_test_emailer.sh..."
		os.system("touch ${HOME}/.jarvs/RVS_test_emailer.sh")
		for line in scripts.rvs_test_emailer:
			command = "echo '" + line + "' | cat >> ${HOME}/.jarvs/RVS_test_emailer.sh"
			os.system(command)

	if not os.path.isfile(home_jarvs + "/RVS_reporter.sh"):
		print "writing RVS_reporter.sh..."
		os.system("touch ${HOME}/.jarvs/RVS_reporter.sh")
		for line in scripts.rvs_reporter:
			command = "echo '" + line + "' | cat >> ${HOME}/.jarvs/RVS_reporter.sh"
			os.system(command)

	if not os.path.isfile(home_jarvs + "/rvsdata.cfg"):
		print "writing rvsdata.cfg..."
		os.system("touch ${HOME}/.jarvs/rvsdata.cfg")
		for index, line in enumerate(scripts.rvs_data_cfg):
			# reverse " and ' for the crazy awk lines that have all kinds of quotes
			#if index < 20 or ( index > 25 and index < 43 ) or index > 49:
			command = "echo '" + line + "' | cat >> ${HOME}/.jarvs/rvsdata.cfg"
			#else:
			#	command = "echo '" + line + "' | cat >> ${HOME}/.jarvs/rvsdata.cfg"
			os.system(command)

def main():
	# only do any of this if no ~/.jarvs directory
	if not os.path.isdir(home_jarvs):
		rvs_scripts = shellscripts.Scripts()
		build(rvs_scripts)

if __name__ == '__main__':       
	main()
