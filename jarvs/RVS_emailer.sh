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

source ./jarvs/rvsdata.cfg
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
  echo "Dr. $name_first $name_last," | cat > email.txt  # initialize txt for email
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
          echo "  $rvspidn from ${rvsdatedash} is OVERDUE" | cat >> premail.txt
        else
          echo "  $rvspidn from ${rvsdatedash} is due ${DUEDATEDASH}" | cat >> premail.txt
        fi
      fi
    done
    parsecount="0"
  done

  echo "You have [${rvscount}] RVSs outstanding. [${rvsoverduecount}] of these are overdue, please approve." | cat >> email.txt    # compose email
  cat premail.txt >> email.txt
  echo "" | cat >> email.txt
  echo "Files are in ${root_dir}/${name_dir}" | cat >> email.txt
  echo "" | cat >> email.txt
  echo "Do not reply to this email, please contact ${name_ccemail} if you have any questions." | cat >> email.txt

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

rm email.txt  # remove email txt files
rm premail.txt
