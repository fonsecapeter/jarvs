#!/usr/bin/env python
import random
from datetime import *

with open('./app/preferences/user_name.txt') as user_name_file:
	global user_name
	user_name = user_name_file.read().rstrip()

def generate_generic_greeting():
	generic = []
	generic.append("Hello, " + user_name + ",")
	generic.append("Hello,")
	generic.append("Hi, there, " + user_name + ",")
	generic.append("Hi, there,")
	generic.append("Sup,")

	return random.choice(generic) 

def generate_morning_greeting():
	morning = []
	morning.append("Good morning, " + user_name + ",")
	morning.append("Good morning,")
	morning.append("Top of the morning to ya,")

	return random.choice(morning)

def generate_afternoon_greeting():
	afternoon = []
	afternoon.append("Good afternoon, " + user_name + ",")
	afternoon.append("Good afternoon,")

	return random.choice(afternoon) 

def generate_evening_greeting():
	evening = []
	evening.append("Good evening, " + user_name + ",")
	evening.append("Good evening,")

	return random.choice(evening)

def generate_night_greeting():
	night = []
	night.append("Still at it, " + user_name + "?")
	night.append("Still at it?")

	return random.choice(night)

def main():

	# decide if generic or tod greeting
	greet_types = ["generic", "tod"]
	greet_type = random.choice(greet_types)

	# return appropriate greeting
	if greet_type is "generic":
		output = generate_generic_greeting()
	else:
		current_hour = datetime.now().hour
		if current_hour > 4 and current_hour < 12:
			output = generate_morning_greeting()
		elif current_hour > 11 and current_hour < 16:
			output = generate_afternoon_greeting()
		elif current_hour > 15 and current_hour < 20:
			output = generate_evening_greeting()
		else:
			output = generate_night_greeting()

	return output

if __name__ == '__main__':
	main()