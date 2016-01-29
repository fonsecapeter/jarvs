# want to output a string of the second line for a greeting
cd ./app/preferences
# get username
user_name=`cat ../preferences/user_name.txt`

# create array of possible generic grettings
generate_generic_greeting () {
generic[0]="How are you doing?"
generic[1]="What can I do for you?"
generic[2]="How can I help?"
generic[3]="Let me know if there is anything you need."
generic[4]="What do you need?"
generic[5]="How may I assist you?"
generic[6]="What do you want?"
generic[7]="Are you about done then?"
generic[8]="What brings you my way?"

generic_length=${#generic[@]}

rand=$[ RANDOM % 2 ]
today=`date +%m-%d`
if [ $today == "01-22" ] && [ $rand == 0 ]; then
		echo "Did you know it's my birthday?"
else
	rand=$[ RANDOM % $generic_length ]
	echo "${generic[$rand]}"
fi
}

generate_generic_greeting

cd ../..