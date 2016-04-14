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

def main():
	import os
	home = os.path.expanduser("~")
	home_jarvs = home + "/.jarvs"

	# only do any of this if no ~/.jarvs directory
	if not os.path.isdir(home_jarvs):
		rvs_scripts = Scripts()
		build(rvs_scripts)

def build(scripts):
	import sqlite3

	# make ~/.jarvs
	try:
		os.makedirs(home_jarvs)
	except OSError as exception:
		if not os.path.isdir(home_jarvs):
			raise
 	# create database
	conn = sqlite3.connect(home_jarvs + "/RVS.db")
	conn.execute("""
			CREATE TABLE Preferences (
			id   INT PRIMARY KEY   NOT NULL,
			username        TEXT   NOT NULL,
			useremail       TEXT   NOT NULL,
			usercolor       TEXT   NOT NULL,
			jarvscolor      TEXT   NOT NULL,
			backgroundcolor TEXT   NOT NULL,
			rootdir         TEXT   NOT NULL);""")

	conn.execute("""
			CREATE TABLE Attendings (
			id   INT PRIMARY KEY   NOT NULL,
			fname           TEXT   NOT NULL,
			lname           TEXT   NOT NULL,
			dirname         TEXT   NOT NULL,
			email           TEXT   NOT NULL);""")

	conn.close()

	# build scripts in ./jarvs
	emailer_cmd = "cat " + scripts.rvs_emailer + " > ${HOME}/.jarvs/RVS_emailer.sh"
	os.system(emailer_cmd)

	test_emailer_cmd = "cat " + scripts.rvs_test_emailer + " > ${HOME}/.jarvs/RVS_test_emailer.sh"
	os.system(test_emailer_cmd)

	reporter_cmd = "cat " + scripts.rvs_reporter + " > ${HOME}/.jarvs/RVS_reporter.sh"
	os.system(reporter_cmd)

	rvs_data_cmd = "cat " + scripts.rvs__data_cfg + " > ${HOME}/.jarvs/rvsdata.cfg"
	os.system(rvs_data_cmd)


class Scripts:
	def __init__(self):
		self.rvs_emailer = """
#!/bin/bash
# PPG RVS emailer by Peter Fonseca
# troubleshooting/development commands denoted by ##
# cron job should be  0 9 * * Wed /<path>/RVS_emailer.sh
# crontab -e opens crontab for editting, choose nano
# crontab -l displays current crontab entries
# * * * * * command to be executed
# - - - - -
#  \ \ \ \ \
#   \ \ \ \ [----- day of week (0-7) (Sunday or Sun = 0)
#    \ \ \ [------ month (1-12)
#     \ \ [------- day of month (1-31)
#      \ [-------- hour (0-23)
#       [--------- minute (0-59)

# get user email the old way
##user_email=`cat ./jarvs/app/preferences/user_email.txt`

source ${HOME}/.jarvs/rvsdata.cfg
# define function to be repeated for every attending
emailer () {
  name_first="$1"
  name_last="$2"
  name_dir="$3"
  name_email="$4"
  name_ccemail="$5"
  root_dir="$6"

  filecount="0"  # initialize variables
  parsecount="0"
  rvscount="0"
  rvsoverduecount="0"
  echo "Dr. $name_first $name_last," | cat > ${HOME}/.jarvs/email.txt  # initialize txt for email
  echo "" | cat > premail.txt
  if [ $OS == "Linux" ] 2> /dev/null; then
    DATE=$(date +%Y%m%d)
  else
    DATE=$(gdate +%Y%m%d)
  fi
  ##echo "today is [$DATE]"

  ##files="$(ls -1 ./Outstanding${name_dir}*RVS*)"
  files="$(ls -1 ${root_dir}/${name_dir}*RVS*)"  # first get all full file names in one var
  arr=$(echo "$files" | tr ";" "\n")  # parse into each short file name
  for x in $arr
  do
    let filecount++
    ##echo "file $filecount"
    arrloop=$(echo "$x" | tr "_" "\n")  # parse each filename to extract pidn and date
    for x in $arrloop
    do
      let parsecount++
       ##echo "parse $parsecount"
      if [ $parsecount -eq 2 ] && [ $x -eq $x ] 2>/dev/null; then
        let rvscount++  # count outstanding rvs's
        ##echo "pidn_$rvscount > [$x]"
        rvspidn=$x  # get pidn
      fi
      if [ $parsecount -eq 3 ]; then
        ##echo "date_$rvscount > [$x]"
          rvsdate=$( echo "$x" | tr -d ".")  # get date for calculation
          rvsdatedash=$( echo "$x" | tr "." "-")  # get date for email
          ##echo "rvsdate $rvsdate"
        if [ $OS == "Linux" ] 2> /dev/null; then
          DUEDATE=$(date -d "$rvsdate 3 weeks" +%Y%m%d)  # calculate due date of 3 weeks after visit for each RVS
          DUEDATEDASH=$(date -d "$DUEDATE" +%Y-%m-%d)
        else
          DUEDATE=$(gdate -d "$rvsdate 3 weeks" +%Y%m%d)  # calculate due date of 3 weeks after visit for each RVS
          DUEDATEDASH=$(gdate -d "$DUEDATE" +%Y-%m-%d)
        fi
        # calculate due date formatted for email
        if [ "$DATE" -ge "$DUEDATE" ]; then
          let rvsoverduecount++  # count overdue rvs's
          echo "  $rvspidn from ${rvsdatedash} is OVERDUE" | cat >> ${HOME}/.jarvs/premail.txt
        else
          echo "  $rvspidn from ${rvsdatedash} is due ${DUEDATEDASH}" | cat >> ${HOME}/.jarvs/premail.txt
        fi
      fi
    done
    parsecount="0"
  done

  echo "You have [${rvscount}] RVSs outstanding. [${rvsoverduecount}] of these are overdue, please approve." | cat >> ${HOME}/.jarvs/email.txt    # compose email
  cat premail.txt >> ${HOME}/.jarvs/email.txt
  echo "" | cat >> ${HOME}/.jarvs/email.txt
  echo "Files are in ${root_dir}/${name_dir}" | cat >> ${HOME}/.jarvs/email.txt
  echo "" | cat >> ${HOME}/.jarvs/email.txt
  echo "Do not reply to this email, please contact ${name_ccemail} if you have any questions." | cat >> ${HOME}/.jarvs/email.txt

  if [ "$rvscount" -gt "0" ]; then
    mail -s "Overdue RVS's" -c "$name_ccemail" "$name_email" < email.txt # send attd email if they have any outstanding RVS's
    echo "> email sent to [${name_email}]"
  fi
}

# ---> Run Emailer Method for all Attendings in RVS.db
# emailer method syntax:
# name_first => first name
# name_last => last name
# name_dir => directory name in hdrive
# name_email => email address

# emailer <name_first> <name_last> <name_dir> <name_email> <name_ccemail>

# att id is the same as the index for each var
for ID in ${attending_ids[@]}; do
  emailer ${attending_fnames[$ID]} ${attending_lnames[$ID]} ${attending_dirnames[$ID]} ${attending_emails[$ID]} ${user_email} ${root_dir}
done

# unit emails without database
##emailer "Elaine" "Benes" "/Benes,Elaine/" "$user_email" "$user_email"
##emailer "George" "Costanza" "/Costanza,George/" "$user_email" "$user_email"
##emailer "Peter" "Fonseca" "/Fonseca,Peter/" "$user_email" "$user_email"
##emailer "Julius" "Hibbert" "/Hibbert,Julius/" "$user_email" "$user_email"
##emailer "Clark" "Kent" "/Kent,Clark/" "$user_email" "$user_email"
##emailer "Cosmo" "Kramer" "/Kramer,Cosmo/" "$user_email" "$user_email"
##emailer "Elizabeth" "Lemon" "/Lemon,Elizabeth/" "$user_email" "$user_email"
##emailer "Lex" "Luthor" "/Luthor,Lex/" "$user_email" "$user_email"
##emailer "Nick" "Riviera" "/Riviera,Nick/" "$user_email" "$user_email"
##emailer "Jerry" "Seinfeld" "/Seinfeld,Jerry/" "$user_email" "$user_email"
##emailer "Bob" "Vance" "/Vance,Bob/" "$user_email" "$user_email"
##emailer "Art" "Vandalay" "/Vandalay,Art/" "$user_email" "$user_email"

rm ${HOME}/.jarvs/email.txt  # remove email txt files
rm ${HOME}/.jarvs/premail.txt
		"""

		self.rvs_reporter = """
#!/bin/bash
# PPG RVS reporter by Peter Fonseca
# adapted from RVS_emailer by Peter Fonseca
# requires empty or existing RVS_report.csv and RVS_vis.py,
# which requires python, pandas, and latest matplotlib
# appends new set of 12 rows to RVS_report.csv
# header is: name,daterported,numrvs,numoverdue
# troubleshooting/development commands denoted by ##

# import RVS.db
source ${HOME}/.jarvs/rvsdata.cfg

# main method
reporter () {
  name_first=$1
  name_dir=$2

filecount="0"
parsecount="0"
rvscount="0"
rvsoverduecount="0"

if [ $OS == "Linux" ] 2> /dev/null; then
  DATE=$(date +%Y%m%d)
  datedash=$(date +%Y-%m-%d)
else
  DATE=$(gdate +%Y%m%d)
  datedash=$(gdate +%Y-%m-%d)
fi
##echo "today is [$DATE]"

# first get all files in one var
##files="$(ls -1 ./Outstanding/$name_dir/*RVS*)"
files="$(ls -1 ${root_dir}/${name_dir}*RVS*)"  # first get all full file names in one var
##echo "files: $files"
# parse into each files
arr=$(echo "$files" | tr ";" "\n")
for x in $arr
do
  let filecount++
  ##echo "file $filecount"
  ##echo "$x"
  # parse each filename to extract pidn and date
  # because of dir/fname structure/convention,
  # 3rd of numericals is pidn, 4th is date
  arrloop=$(echo "$x" | tr "_" "\n")
  ##echo "arrloop: $arrloop"
  for x in $arrloop
  do
    let parsecount++
     #echo "parse $parsecount"
    if [ $parsecount -eq 2 ] && [ $x -eq $x ] 2>/dev/null; then
      # count outstanding rvs's
      let rvscount++
      ##echo "pidn_$rvscount > [$x]"
    fi
    if [ $parsecount -eq 3 ]; then
      ##echo "date_$rvscount > [$x]"
        # format date for math
        rvsdate=$( echo "$x" | tr -d ".")
        ##echo "rvsdate_$rvscount > [$rvsdate]"
      # calculate due date of 6 months after visit
      # for each rvs
      # gdate for mac, date for linux
      # must brew install coreutils to use gdate
      if [ $OS == "Linux" ] 2> /dev/null; then
        DUEDATE=$(date -d "$rvsdate 6 months" +%Y%m%d)
      else
        DUEDATE=$(gdate -d "$rvsdate 6 months" +%Y%m%d)
      fi
      ##echo "due: $DUEDATE"
      if [ "$DATE" -ge "$DUEDATE" ]; then
        # count overdue rvs's
        let rvsoverduecount++
        echo "> $name_first_[$rvscount] is overdue"
      fi
    fi
  done
  parsecount="0"
done

# make new report if current one gets to be too big
if [[ $(wc -l <./jarvs/RVS_report.csv) -ge 1000 ]]; then
  mv "${HOME}/.jarvs/RVS_report.csv" ".${HOME}/.jarvs/old_reports/RVS_report_${datedash}.csv"
  touch ${HOME}/.jarvs/RVS_report.csv
fi

# append new line to RVS_report.csv with attending's notes
echo "$name_first,$datedash,$rvscount,$rvsoverduecount"  >> ${HOME}/.jarvs/RVS_report.csv
echo "> $name_first's RVS's reported on [$datedash]"
}


# ---> Run reporter Method for all Attendings in RVS.db
# reporter method syntax:
# name_first = first name
# name_dir = attendings directory

# reporter <name_first> <name_dir>

# att id is the same as the index for each var
for ID in ${attending_ids[@]}; do
  reporter ${attending_fnames[$ID]} ${attending_dirnames[$ID]}
done

# visualize the RVS_report.csv
${HOME}/.jarvs//RVS_vis.py
		"""

		self.rvs_test_emailer = """
#!/bin/bash
# PPG RVS test-emailer by Peter Fonseca
# troubleshooting/development commands denoted by ##
# cron job should be  0 9 * * Wed /<path>/RVS_emailer.sh
# crontab -e opens crontab for editting, choose nano
# crontab -l displays current crontab entries
# * * * * * command to be executed
# - - - - -
#  \ \ \ \ \
#   \ \ \ \ [----- day of week (0-7) (Sunday or Sun = 0)
#    \ \ \ [------ month (1-12)
#     \ \ [------- day of month (1-31)
#      \ [-------- hour (0-23)
#       [--------- minute (0-59)

# get user email the old way
##user_email=`cat ./jarvs/app/preferences/user_email.txt`

# import RVS.db
source ${HOME}/.jarvs/rvsdata.cfg

# define function to be repeated for every attending
emailer () {
  name_first="$1"
  name_last="$2"
  name_dir="$3"
  name_email="$4"
  name_ccemail="$5"

filecount="0"  # initialize variables
parsecount="0"
rvscount="0"
rvsoverduecount="0"
echo "Dr. $name_first $name_last," | cat > {HOME}/.jarvs/email.txt  # initialize txt for email
echo "" | cat > {HOME}/.jarvs/premail.txt
if [ $OS == "Linux" ] 2> /dev/null; then
  DATE=$(date +%Y%m%d)
else
  DATE=$(gdate +%Y%m%d)
fi
##echo "today is [$DATE]"

##files="$(ls -1 ./Outstanding${name_dir}*RVS*)"
files="$(ls -1 ${root_dir}/${name_dir}*RVS*)"  # first get all full file names in one var
arr=$(echo "$files" | tr ";" "\n")  # parse into each short file name
for x in $arr
do
  let filecount++
  ##echo "file $filecount"
  arrloop=$(echo "$x" | tr "_" "\n")  # parse each filename to extract pidn and date
  for x in $arrloop
  do
    let parsecount++
     ##echo "parse $parsecount"
    if [ $parsecount -eq 2 ] && [ $x -eq $x ] 2>/dev/null; then
      let rvscount++  # count outstanding rvs's
      ##echo "pidn_$rvscount > [$x]"
      rvspidn=$x  # get pidn
    fi
    if [ $parsecount -eq 3 ]; then
      ##echo "date_$rvscount > [$x]"
        rvsdate=$( echo "$x" | tr -d ".")  # get date for calculation
        rvsdatedash=$( echo "$x" | tr "." "-")  # get date for email
        ##echo "rvsdate $rvsdate"
      if [ $OS == "Linux" ] 2> /dev/null; then
        DUEDATE=$(date -d "$rvsdate 3 weeks" +%Y%m%d)  # calculate due date of 3 weeks after visit for each RVS
        DUEDATEDASH=$(date -d "$DUEDATE" +%Y-%m-%d)
      else
        DUEDATE=$(gdate -d "$rvsdate 3 weeks" +%Y%m%d)  # calculate due date of 3 weeks after visit for each RVS
        DUEDATEDASH=$(gdate -d "$DUEDATE" +%Y-%m-%d)
      fi
      # calculate due date formatted for email
      if [ "$DATE" -ge "$DUEDATE" ]; then
        let rvsoverduecount++  # count overdue rvs's
        echo "  $rvspidn from ${rvsdatedash} is OVERDUE" | cat >> {HOME}/.jarvs/premail.txt
      else
        echo "  $rvspidn from ${rvsdatedash} is due ${DUEDATEDASH}" | cat >> {HOME}/.jarvs/premail.txt
      fi
    fi
  done
  parsecount="0"
done

echo "You have [${rvscount}] RVS's outstanding. [${rvsoverduecount}] of these are overdue, please approve." | cat >> {HOME}/.jarvs/email.txt    # compose email
cat premail.txt >> {HOME}/.jarvs/email.txt
echo "" | cat >> {HOME}/.jarvs/email.txt
##echo 'Files are in rvs/Outstanding/'${name_first}','${name_last} | cat >> {HOME}/.jarvs/email.txt
echo "Files are in ${root_dir}/${name_dir}" | cat >> {HOME}/.jarvs/email.txt
echo "" | cat >> {HOME}/.jarvs/email.txt
echo "Do not reply to this email, please contact ${name_ccemail} if you have any questions." | cat >> {HOME}/.jarvs/email.txt

if [ "$rvscount" -gt "0" ]; then
  mail -s "Overdue RVS's" -c "$name_ccemail" "$name_email" < email.txt # send attd email if they have any outstanding RVS's
  echo "> email sent to [${name_email}]"
fi
}

# ---> Run Emailer Method for all Attendings in RVS.db
# emailer method syntax:
# name_first => first name
# name_last => last name
# name_dir => directory name in hdrive
# name_email => email address

# emailer <name_first> <name_last> <name_dir> <name_email> <name_ccemail>

# att id is the same as the index for each var
for ID in ${attending_ids[@]}; do
	emailer ${attending_fnames[$ID]} ${attending_lnames[$ID]} ${attending_dirnames[$ID]} $user_email $user_email
done

# unit emails without database
##emailer "Elaine" "Benes" "/Benes,Elaine/" "$user_email" "$user_email"
##emailer "George" "Costanza" "/Costanza,George/" "$user_email" "$user_email"
##emailer "Peter" "Fonseca" "/Fonseca,Peter/" "$user_email" "$user_email"
##emailer "Julius" "Hibbert" "/Hibbert,Julius/" "$user_email" "$user_email"
##emailer "Clark" "Kent" "/Kent,Clark/" "$user_email" "$user_email"
##emailer "Cosmo" "Kramer" "/Kramer,Cosmo/" "$user_email" "$user_email"
##emailer "Elizabeth" "Lemon" "/Lemon,Elizabeth/" "$user_email" "$user_email"
##emailer "Lex" "Luthor" "/Luthor,Lex/" "$user_email" "$user_email"
##emailer "Nick" "Riviera" "/Riviera,Nick/" "$user_email" "$user_email"
##emailer "Jerry" "Seinfeld" "/Seinfeld,Jerry/" "$user_email" "$user_email"
##emailer "Bob" "Vance" "/Vance,Bob/" "$user_email" "$user_email"
##emailer "Art" "Vandalay" "/Vandalay,Art/" "$user_email" "$user_email"


rm {HOME}/.jarvs/email.txt  # remove email txt files
rm {HOME}/.jarvs/premail.txt
		"""

		self.rvs_data_cfg = """
#!/bin/bash
# fetch data from RVS.db
# adapted from andreaolivato.tumblr.com/post/133473114/using-sqlite3-in-bash
# also has info on making and cruding tables/db's

# get all the data
LIST=`sqlite3 {HOME}/.jarvs/RVS.db "SELECT * FROM Attendings"`

##echo "ID > FNAME > LNAME > DIRNAME > EMAIL"

# declare arrays to store the data in memory, the index will be the id
attending_ids=()
attending_fnames=()
attending_lnames=()
attending_dirnames=()
attending_emails=()

# for each row...
for ROW in $LIST; do
	# parse data (sqlite returns a pip separated string by default)
	ID=`echo $ROW | awk '{split($0,a,"|"); print a[1]}'`
	FNAME=`echo $ROW | awk '{split($0,a,"|"); print a[2]}'`
	LNAME=`echo $ROW | awk '{split($0,a,"|"); print a[3]}'`
	DIRNAME=`echo $ROW | awk '{split($0,a,"|"); print a[4]}'`
	EMAIL=`echo $ROW | awk '{split($0,a,"|"); print a[5]}'`

	# print the data
	##echo $ID" > "$FNAME" > "$LNAME" > "$DIRNAME" > "$EMAIL
	# append the data to each array
	attending_ids+=($ID)
	attending_fnames+=($FNAME)
	attending_lnames+=($LNAME)
	attending_dirnames+=($DIRNAME)
	attending_emails+=($EMAIL)
done

##echo "number of attendings: "${#attending_ids[@]}
##echo "attending ids: "${attending_ids[@]}
##echo "attending first names: "${attending_fnames[@]}
##echo "attending last names: "${attending_lnames[@]}
##echo "attending directory names: "${attending_dirnames[@]}
##echo "attending emails: "${attending_emails[@]}

##echo "Adam Boxer: ID="${attending_ids[0]}" FNAME="${attending_fnames[0]}" LNAME="${attending_lnames[0]}" DIRNAME="${attending_dirnames[0]}" EMAIL="${attending_emails[0]}

##echo ""

# same for preferences
# onle one entry, but just take array[0] as var

LIST=`sqlite3 ./jarvs/RVS.db "SELECT * FROM Preferences"`

##echo "USERNAME > USEREMAIL > USERCOLOR > JARVSCOLOR > BACKGROUNDCOLOR"

user_id=()
user_names=()
user_emails=()
user_colors=()
jarvs_colors=()
background_colors=()

for ROW in $LIST; do
	ID=`echo $ROW | awk '{split($0,a,"|"); print a[1]'`
	USERNAME=`echo $ROW | awk '{split($0,a,"|"); print a[2]}'`
	USEREMAIL=`echo $ROW | awk '{split($0,a,"|"); print a[3]}'`
	USERCOLOR=`echo $ROW | awk '{split($0,a,"|"); print a[4]}'`
	JARVSCOLOR=`echo $ROW | awk '{split($0,a,"|"); print a[5]}'`
	BACKGROUNDCOLOR=`echo $ROW | awk '{split($0,a,"|"); print a[6]}'`

	# print the data
	##echo $USERNAME" > "$USEREMAIL" > "$USERCOLOR" > "$JARVSCOLOR" > "$BACKGROUNDCOLOR

	user_ids+=($ID)
	user_names+=($USERNAME)
	user_emails+=($USEREMAIL)
	user_colors+=($USERCOLOR)
	jarvs_colors+=($JARVSCOLOR)
	background_colors+=($BACKGROUNDCOLOR)
done

user_id=${user_ids[0]}
user_name=${user_names[0]}
user_email=${user_emails[0]}
user_color=${user_colors[0]}
jarvs_color=${jarvs_colors[0]}
background_color=${background_colors[0]}
		"""

if __name__ == '__main__':       
	main()
