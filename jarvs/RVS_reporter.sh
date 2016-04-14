#!/bin/bash
# PPG RVS reporter by Peter Fonseca
# adapted from RVS_emailer by Peter Fonseca
# requires empty or existing RVS_report.csv and RVS_vis.py,
# which requires python, pandas, and latest matplotlib
# appends new set of 12 rows to RVS_report.csv
# header is: name,daterported,numrvs,numoverdue
# troubleshooting/development commands denoted by ##

# import RVS.db
source ./jarvs/rvsdata.cfg

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
  mv "./jarvs/RVS_report.csv" "./jarvs/old_reports/RVS_report_${datedash}.csv"
  touch ./jarvs/RVS_report.csv
fi

# append new line to RVS_report.csv with attending's notes
echo "$name_first,$datedash,$rvscount,$rvsoverduecount"  >> ./jarvs/RVS_report.csv
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
./jarvs/RVS_vis.py
