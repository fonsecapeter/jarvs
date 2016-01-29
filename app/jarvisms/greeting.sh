# want to output a string of randomly pieced together greeting

# get username
user_name=`cat ../preferences/user_name.txt`

# create array of possible generic grettings
generate_generic_greeting () {
generic[0]="Hello, ${user_name},"
generic[1]="Hello,"
generic[2]="Hi, there, ${user_name},"
generic[3]="Sup,"

generic_length=${#generic[@]}

rand=$[ RANDOM % $generic_length ]
echo "${generic[$rand]}"
}

# create array of possible morning greetings
generate_morning_greeting () {
morning[0]="Good morning, ${user_name},"
morning[1]="Good morning,"

morning_length=${#morning[@]}

rand=$[ RANDOM % $morning_length ]
echo "${morning[$rand]}"
}

# do same for afternoon
generate_afternoon_greeting () {
afternoon[0]="Good afternoon, ${user_name},"
afternoon[1]="Good afternoon"

afternoon_length=${#afternoon[@]}

rand=$[ RANDOM % $afternoon_length ]
echo "${afternoon[$rand]}"
}

# do same for evening
generate_evening_greeting () {
evening[0]="Good evening, ${user_name},"
evening[1]="Good evening,"

evening_length=${#evening[@]}

rand=$[ RANDOM % $evening_length ]
echo "${evening[$rand]}"
}

# do same for night
generate_night_greeting () {
night[0]="Still at it, ${user_name}?"
night[1]="Still at it?"

night_length=${#night[@]}

rand=$[ RANDOM % $night_lenght ]
echo "${night[$rand]}"
}

# decide if generic or tod greeting
rand=$[ RANDOM % 2 ]
if [ $rand == 0 ]; then
	greet_type="generic"
else
	greet_type="tod"
fi


if [ $greet_type == "tod" ]; then
	generate_generic_greeting
else
	# decide time of day
	if [ $OS == "Linux" ]; then
		h=`date +%H`
	else
		h=`gdate +%H`
	fi

	if [ $h -gt 4 ] && [ $h -lt 12 ]; then
		tod="morning"
	elif [ $h -gt 11 ] && [ $h -lt 16 ]; then
		tod="afternoon"
	elif [ $h -gt 15 ] && [ $h -lt 20 ]; then
		tod="evening"
	else
		tod="night"
	fi

	# display appropriate greeting
	if [ $tod == "morning" ]; then
		generate_morning_greeting
	elif [ $tod == "afternoon" ]; then
		generate_afternoon_greeting
	elif [ $tod == "evening" ]; then
		generate_evening_greeting
	else
		generate_night_greeting
	fi
fi