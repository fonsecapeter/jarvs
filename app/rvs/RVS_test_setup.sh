#!/bin/bash
# this script will create a local test
# directory set with one folder for each
# attending, containing rvs's of varying age
# this is meant to run BEFORE using the
# other scripts to set up an environment of
# rvs's and attendings
# written by Peter Fonseca

# make an array of the 12 fake doctors directory names
attds[0]="Vandalay,Art"
attds[1]="Hibbert,Julius"
attds[2]="Riviera,Nick"
attds[3]="Vance,Bob"
attds[4]="Fonseca,Peter"
attds[5]="Kramer,Cosmo"
attds[6]="Seinfeld,Jerry"
attds[7]="Costanza,George"
attds[8]="Benes,Elaine"
attds[9]="Luthor,Lex"
attds[10]="Kent,Clark"
attds[11]="Lemon,Elizabeth"

# make aux dirs for realism
# and add links
# use $PWD instead of . to avoid
# creating too many levels of symbolic links
mkdir "./app/rvs/Outstanding"

mkdir "./app/rvs/Outstanding/DONE"
ln -s "${PWD}/app/rvs/Converted" "${PWD}/app/rvs/Outstanding/DONE/Converted"

mkdir "./app/rvs/Converted"
ln -s "${PWD}/app/rvs/Uploaded" "${PWD}/app/rvs/Converted/Uploaded"

mkdir "./app/rvs/Uploaded"

# loop through attendings
for i in "${attds[@]}"; do
	# create dir for each attd
	mkdir "./app/rvs/Outstanding/${i}"

	# insert link to DONE
	ln -s "${PWD}/app/rvs/DONE" "${PWD}/app/rvs/Outstanding/${i}/DONE"

	# generate random number of test rvs's
	# and create them with some random info
	# in this case no more than 14
	# for each attd
	r=$RANDOM
	let "r %= 14"
	counter=0
	while [ $counter -lt $r ]; do
		# set the random values for filenames
		Year=$(date +%Y)

		Mo=0
		while [ $Mo -le 0 ]; do
			Mo=$RANDOM
			if [ $(date +%m) -lt 6 ]; then
				let "Mo %= 12"
				let "Year -= 1"
			else
				let "Mo %= $(date +%m)"
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

		ID=0
		while [ $ID -le 0 ]; do
			ID=$RANDOM
			let "ID %= 30000"
		done

		# create the file
		touch "./app/rvs/Outstanding/$i/lname, fname_${ID}_${Year}.${Mo}.${Day}_RVS.doc"

		# Unit Tests
		##echo "Year: $Year"
		##echo "Mo: $Mo"
		##echo "Day: $Day"
		##echo "ID: $ID"
		echo " > ./app/rvs/Outstanding/${i}/${ID}"

		let counter++
	done

	let i++
done

touch "./app/rvs/RVS_report.csv"
