#!/bin/bash
# syntax: jarvs <command>
# to do:
#  * build initial menu framework
#  * set arguments for running the big three
#  * set arguments for other useful commands
#  * maintain list of <command> s

set_name () {
	echo "Do you usually go by ${USER}?"
	contin="yes"
	while [ $contin == "yes" ]; do
		read name_resp

		case "$name_resp" in
			"yes")
				echo "Great, I thought so."
				echo "$USER" > ./app/preferences/user_name.txt
				contin="no"
				break
			;;
			"no")
				echo "How would you prefer I address you?"
				read user_name
				echo "$user_name" > ./app/preferences/user_name.txt
				echo "Thanks, ${user_name}, I'll be sure to make"
				echo "note of that."
				contin="no"
				break
			;;
			*)
				echo "My apologies, I don't understand that."
				echo "Try typing yes or no in lower-case."
				contin="yes"
			;;
		esac
	done
	user_name=`cat ./app/preferences/user_name.txt`
}

set_color () {
	echo "What is your favorite color?"
	sleep 1s
	echo "choices are:"
	sleep 1s
	tput setaf 1
	echo "red"
	sleep 1s
	tput setaf 2
	echo "green"
	sleep 1s
	tput setaf 3
	echo "orange"
	sleep 1s
	tput setaf 4
	echo "blue"
	sleep 1s
	tput setaf 5
	echo "purple"
	sleep 1s
	tput setaf 6
	echo "light-blue"
	sleep 1s
	tput setaf 7
	echo "white"
	tput sgr0
	read fav_clr

	case "$fav_clr" in
		red)
			echo "1" > ./app/preferences/clr.txt
		;;

		green)
			echo "2" > ./app/preferences/clr.txt
		;;

		orange)
			echo "3" > ./app/preferences/clr.txt
		;;

		blue)
			echo "4" > ./app/preferences/clr.txt
		;;

		purple)
			echo "5" > ./app/preferences/clr.txt
		;;

		light-blue)
			echo "6" > ./app/preferences/clr.txt
		;;

		white)
			echo "7" > ./app/preferences/clr.txt
		;;

		*)
			echo "I'm sorry, I don't know that one."
			echo "Try typing your color in lower-case."
		;;
	esac

	clr=`cat ./app/preferences/clr.txt`
	tput setaf $clr
		echo "Much better, Thanks!"
		sleep 3s
		echo "If you ever change your mind,"
		echo "just ask me to change your preferences."
	tput sgr0
}

set_email () {
	echo "What is your email address?"
	sleep 2s
	echo "Don't worry, I wont spam you with promotions."
	read user_email
	echo "Got it."
	echo "${user_email}" > ./app/preferences/user_email.txt
	user_email=`cat ./app/preferences/user_email.txt`
}

# if first time using jarvs, set preferences
if [ ! -f ./app/preferences/clr.txt ]; then
	if [ ! -d ./app/preferences ]; then
		mkdir ./app/preferences
	fi
	echo "Hello, ${USER}"
	sleep 3s
	echo "My name is Jarvs, and I am your personal assistant."
	sleep 2s
	echo "Peter built me to help manage the rvs program."
	echo "I hope you find that I make life easier."
	sleep 3s
	echo "Before we get started, I have a few questions for you."
	set_name
	echo "Also,"
	set_email
	echo "Lastly:"
	set_color
fi

if [ ! -d ./app/rvs/Outstanding ]; then
	tput setaf $clr
	echo "I'm going to set up the rvs-clone."
	sleep 3s
	./app/rvs/RVS_test_setup.sh
	tput sgr0
fi

user_name=`cat ./app/preferences/user_name.txt`
user_email=`cat ./app/preferences/user_email.txt`
clr=`cat ./app/preferences/clr.txt`

puts () {
	output=$1
	tput setaf $clr
		echo "$1"
	tput sgr0
}

puts "Hello, ${user_name}. What can I help you with?"

menu="main"

# put all menu's in infinite loop ----------------------
while true; do

	# main menu ----------------------------------------
	while [ $menu == "main" ]; do
		read cmd

		case "$cmd" in

			*"list"*)
				puts "<bye> <help> <list> <preferences> <eamil> <report>"
				puts "<date> <agenda> <weather>"
				continue
			;;

			*"help"*)
				puts "I am your personal assistant, you can call me Jarvs."
				puts "Peter built me to help you manage the rvs program."
				puts "All you have to do is give me a command."
				puts "Ask me for a list to see what commands I am programmed"
				puts "to understand"
				puts "You can always tell me to take a break by saying bye."
				continue
			;;

			*)
				prev_menu="$menu"
				menu="utils"
				break
			;;
		esac
	done

	# utilities menu ----------------------------------------
	while [ $menu == "utils" ]; do
		case $cmd in

			*"bye"*)
				puts "Goodbye, let me know if you need anything else."
				exit
			;;

			*"done"*|*"nothing"*|*"main"*)
				puts "Fantastic, what else can I do for you?"
				menu="main"
				break
			;;

			*"list"*)
				puts "<bye> <help> <list> <preferences> <eamil> <report>"
				puts "<date> <agenda> <weather>"
				continue
			;;

			# linux weather-util & weather-util-data, mac need ansiweather?
			*"weather"*|*"forecast"*)
				echo ""
				tput setaf $clr
				weather 94158
				tput sgr0
				echo ""
			;;


			*"date"*|*"cal"*)
				puts "Always good to stay oriented."
				echo ""
				tput setaf $clr
				cal
				tput sgr0
				echo ""
			;;

			# need to download icalbuddy and test on mac
			*"today"*)
				puts "Here is your agenda for the day:"
				echo ""
				tput setaf $clr
				icalbuddy -f -sc eventsToday
				tput sgr0
				echo ""
			;;

			*"preference"*)
				puts "I do appreciate feedback."
				menu="preferences"
				break
			;;

			*"report"*)
				puts "Of course, I am programmed to tell you how the attendings are doing."
				menu="report"
				break
			;;

			*"email"*)
				puts "Of course, I am programmed to help you send emails."
				menu="email"
				break
			;;

			*"rvs manager"*)
				puts "You must be the rvs manager, a clinical research"
				puts "coordinator responsible for overseeing the rvs program."
				puts "It is crucial to ensure that every note is written,"
				puts "approved, sent, and archived. This can be a source of"
				puts "contention if it is not running smoothly. Particpants"
				puts "contribute a full week of 9-5 work, often including"
				puts "specimen donation and a flight across the country. The"
				puts "rvs is one ofthe only ways we can give back. Along that"
				puts "vein, the advice within is not clinically relevent after"
				puts "6 months and there are many governing rules to what can"
				puts "disclosed. The rvs manager must make sure the center is"
				puts "complient and efficient."
				puts ""
				puts "This task is greater than anticipated, especially considering"
				puts "the growth of the study, so Peter made me to help. I can"
				puts "currently assist on the attending side of things, producing"
				puts "and logging reports, as well as sending weekly reminders to"
				puts "any attending with at least one outstanding rvs."
				puts ""
				puts "A graphical explanation of the flow of an rvs can be seen here:"
				# first instance of linux vs os compatibility
				if [ $OS == "Linux" ]; then
					# 2> /dev/null suppresses error notifications
					eog ./app/rvs/sample_docs/rvs_lifecycle.png 2> /dev/null
				else
					open ./app/rvs/sample_docs/rvs_lifecycle.png
				fi
				puts "This follows the life of 12377's rvs from January 4th, 2016."
				puts "I would've sent Dr. Hibbert this email:"
				echo ""
				tput setaf $clr
				cat ./sample_email.txt
				tput sgr0
				echo ""
				puts "---------------------------"
				echo ""
				puts "I also would've shown you this report:"
				if [ $OS == "Linux" ]; then
					# 2> /dev/null suppresses error notifications
					eog ./app/rvs/sample_docs/figure_1.png 2> /dev/null
				else
					open ./app/rvs/sample_docs/figure_1.png
				fi
			;;


			*"what is"*"rvs"*)
				puts "An rvs is a research visit summary."
				puts "It includes the entire life-hisotry of the particpant"
				puts "in a semi-standard fashion, organized by history of"
				puts "present illness, medical history, social history, family"
				puts "history, lab testing, imaging, and more."
				puts "These rvs's make up a vital resource for researchers and"
				puts "participants. Each participant gets a copy of their rvs"
				puts "and lists a primary doctor (or doctors) who also get a"
				puts "copy. The research center serves as a team of experts"
				puts "devoted to diseases that are otherwise not well-described"
				puts "or are rare, so their advice is cliniclally relevent to"
				puts "the participant's continued clinical care."
				puts "In a large research project, many research participants"
				puts "come in for visits. During a visit, the participant will"
				puts "see different researchers and clinicians. A visit is"
				puts "always overseen by an attending physician (attending), who"
				puts "must give final approval of the rvs."
			;;

			*"thank"*)
				puts "No need to thank me, it's my job."
			;;

			*"how are you"*)
				puts "I can't complain"
			;;

			*)
				puts "I'm terribly sorry, I didn't understand that."
				puts "Try typing help, list, done, or bye."
				puts "Make sure you are typing in lower-case."
			;;
		esac

		menu="$prev_menu"
		break
	done

	# preferences menu ----------------------------------------
	while [ $menu == "preferences" ]; do
		puts "What can I do differently?"
		read cmd

		case $cmd in

			*"color"*)
				set_color
				continue
			;;

			*"name"*)
				set_name
				continue
			;;

			*"email"*)
				set_email
				continue
			;;

			*"list"*)
				puts "<email> <color> <name>"
				puts "<bye> <help> <list> <eamil> <report>"
				puts "<date> <agenda> <weather>"
				continue
			;;

			*"help"*)
				puts "You last told me that wanted to edit your preferences."
				puts "If you need something else, just let me know."
				continue
			;;

			*)
				prev_menu="$menu"
				menu="utils"
				break
			;;
		esac
	done

	# reporting menu ----------------------------------------
	while [ $menu == "report" ]; do

		puts "How can I help you with reporting?"
		read cmd

		case $cmd in

			*"report"*)
				puts "No problem, let me crunch the numbers."
				puts "I'll show you all the rvs's currently waiting"
				puts "for approval"
				tput setaf $clr
				if [ -f ./RVS_reporter.sh ]; then
					./RVS_reporter.sh
				else
					./app/rvs/RVS_reporter.sh
				fi
				tput sgr0
				continue
			;;

			*"vis"*)
				puts "No problem, let me crunch the numbers."
				puts "I'll show you all the rvs's waiting for approval"
				puts "since the last time I reported."
				puts "I won't log the data on this one"
				tput setaf $clr
				if [ -f ./RVS_vis.py ]; then
					./RVS_vis.py
				else
					./app/rvs/RVS_vis.py
				fi
				tput sgr0
				continue
			;;

			*"list"*)
				puts "<report> <vis>"
				puts "<bye> <help> <list> <preferences> <eamil>"
				puts "<date> <agenda> <weather>"
				continue
			;;

			*"help"*)
				puts "You last told me that wanted some help reporting."
				puts "If you need something else, just let me know."
				continue
			;;

			*)
				prev_menu="$menu"
				menu="utils"
				break
			;;
		esac
	done

	# emailing menu ----------------------------------------
	while [ $menu == "email" ]; do
		puts "How can I help you with emails?"
		read cmd

		case $cmd in

			*"email"*)
				puts "No problem, let me write these up."
				tput setaf $clr
				if [ -f ./RVS_emailer.sh ]; then
					./RVS_emailer.sh
				else
					./app/rvs/RVS_emailer.sh
				fi
				tput sgr0
				continue
			;;

			*"list"*)
				puts "<email>"
				puts "<bye> <help> <list> <preferences> <report>"
				puts "<date> <agenda> <weather>"
				continue
			;;

			*"help"*)
				puts "You last told me that wanted some help sending emails."
				puts "If you need something else, just let me know."
				continue
			;;

			*)
				prev_menu="$menu"
				menu="utils"
				break
			;;
		esac
	done

done
