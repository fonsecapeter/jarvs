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
		conn.execute('INSERT INTO Preferences VALUES (0, "Peter", "peter.nfonseca@gmail.com", "#e6e6e6", "#e29d36", "#2c303e", "/home/pfonseca/jarvs/app/rvs/");')
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
		conn.execute('INSERT INTO Attendings VALUES (0, "Peter", "Fonseca", "PeterFonseca", "peter.nfonseca@gmail.com");')
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
			command = 'echo "' + line + '" | cat >> ${HOME}/.jarvs/RVS_emailer.sh'


	if not os.path.isfile(home_jarvs + "/RVS_test_emailer.sh"):
		print "writing RVS_test_emailer.sh..."
		os.system("touch ${HOME}/.jarvs/RVS_test_emailer.sh")
		for line in scripts.rvs_test_emailer:
			command = 'echo "' + line + '" | cat >> ${HOME}/.jarvs/RVS_test_emailer.sh'

	if not os.path.isfile(home_jarvs + "/RVS_reporter.sh"):
		print "writing RVS_reporter.sh..."
		os.system("touch ${HOME}/.jarvs/RVS_reporter.sh")
		for line in scripts.rvs_reporter:
			command = 'echo "' + line + '" | cat >> ${HOME}/.jarvs/RVS_reporter.sh'

	if not os.path.isfile(home_jarvs + "/rvsdata.cfg"):
		print "writing rvsdata.cfg..."
		os.system("touch ${HOME}/.jarvs/rvsdata.cfg")
		for line in scripts.rvs_data_cfg:
			command = 'echo "' + line + '" | cat >> ${HOME}/.jarvs/rvsdata.cfg'

def main():
	# only do any of this if no ~/.jarvs directory
	if not os.path.isdir(home_jarvs):
		rvs_scripts = shellscripts.Scripts()
		build(rvs_scripts)

if __name__ == '__main__':       
	main()
