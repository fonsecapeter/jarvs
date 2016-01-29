# want to output a string of randomly pieced together greeting
# decide time of day
if [ $OS == "linux" ]; then
	h=`date +%H`
else
	h=`gdate +%H`
fi

if [ $h -gt 4 ] && [ $h -lt 12 ]; then
	tod="morning"
else if [ $h -gt 11 ] && [ $h -lt 16 ]; then
	tod="afternoon"
else if [ $h -gt 15 ] && [ $h -lt 4 ]; then
	tod="night"
fi

# get username

# create array of possible morning greetings
morning[0]="Good morning"
morning[1]="Hello there"

morning_length=`#morning[@]`
# generate random number
rand=$[ $RANDOM % morning_length ]
echo ${mornging[$rand]}