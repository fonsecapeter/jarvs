#!/bin/bash
# this script will create a local test
# directory set with one folder for each
# attending, containing rvs's of varying age
# this is meant to run BEFORE using the
# other scripts to set up an environment of
# rvs's and attendings
# written by Peter Fonseca

# import RVS.db
source RVS_db_data_fetch.cfg

# make an array of the 12 fake doctors directory names
##attds[0]="Vandalay,Art"
##attds[1]="Hibbert,Julius"
##attds[2]="Riviera,Nick"
##attds[3]="Vance,Bob"
##attds[4]="Fonseca,Peter"
##attds[5]="Kramer,Cosmo"
##attds[6]="Seinfeld,Jerry"
##attds[7]="Costanza,George"
##attds[8]="Benes,Elaine"
##attds[9]="Luthor,Lex"
##attds[10]="Kent,Clark"
##attds[11]="Lemon,Elizabeth"

# make aux dirs for realism
# and add links
# use $PWD instead of . to avoid
# creating too many levels of symbolic links

mkdir "./Outstanding"

mkdir "./Outstanding/DONE"
ln -s "${PWD}/Converted" "${PWD}/Outstanding/DONE/Converted"

mkdir "./Converted"
ln -s "${PWD}/Uploaded" "${PWD}/Converted/Uploaded"

mkdir "./Uploaded"

# loop through attendings
for ID in ${attending_ids[@]}; do
	echo "./Outstanding${attending_dirnames[$ID]}"
	# delete dir if already exists (reset if using after first time)
	rm -rf "./Outstanding${attending_dirnames[$ID]}"
	# create dir for each attd
	mkdir "./Outstanding${attending_dirnames[$ID]}"
	# insert link to DONE
	ln -s "${PWD}/DONE" "${PWD}/Outstanding${attending_dirnames[$ID]}DONE"

	# generate random number of test rvs's
	# and create them with some random info
	# in this case no more than 14
	# for each attd
	r=$RANDOM
	let "r %= 14"
	counter=0
	while [ $counter -lt $r ]; do
		# set the random values for filenames
		##echo $counter
		if [ $OS == "Linux" ] 2> /dev/null; then
			Year=$(date +%Y)
		else
			Year=$(gdate +%Y)
		fi

		Mo=0
		while [ $Mo -le 0 ]; do
			Mo=$RANDOM
			if [ $OS == "Linux" ] 2> /dev/null; then
				if [ $(date +%m) -lt 6 ]; then
					let "Mo %= 12"
					let "Year -= 1"
				else
					let "Mo %= $(date +%m)"
				fi
			else
				if [ $(gdate +%m) -lt 6 ]; then
					let "Mo %= 12"
					let "Year -= 1"
				else
					let "Mo %= $(gdate +%m)"
				fi
			fi
		done
		if [ $Mo -le 9 ]; then
			Mo="0$Mo"
		fi

		Day=0
		while [ $Day -le 0 ]; do
			Day=$RANDOM
			let "Day %= 28"
		done
		if [ $Day -le 9 ]; then
			Day="0${Day}"
		fi
		PTID=0
		while [ $PTID -le 0 ]; do
			PTID=$RANDOM
			let "PTID %= 30000"
		done
		# create the file
		touch "./Outstanding${attending_dirnames[$ID]}lname, fname_${PTID}_${Year}.${Mo}.${Day}_RVS.doc"

		# Unit Tests
		##echo "Year: $Year"
		##echo "Mo: $Mo"
		##echo "Day: $Day"
		##echo "ID: $ID"
		echo " > ./Outstanding${attending_dirnames[$ID]}${ID}"

		let counter++
	done

	let i++
done

touch "./RVS_report.csv"
