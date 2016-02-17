#!/usr/bin/env python
# Jarvs has a chipper personality
# and doesn't say the same thing every time.
# This is because Jarvs uses a library of
# Jarvisms that are randomly selected
# and sometimes dynamically chosen based on the time of day
# To use, import jarvisms (which should be inthe same
# dir as the script in which it is imported)
# then call jarvisms.<function>() where you would
# like a jarvism returned.
# for example, "print jarvisms.signoff()" should
# print something like "Farewell for now."
# to the screen.
#
# Created by Peter Fonseca for use in the Jarvs python gui,
# re-written and expanded from the original bash scripts
#
# structure is:
#   > Unit Methods: methods intended for use in core methods
#   > Core Methods: methods intended for use when imported
import random
from datetime import *

# read username from saved preference file
with open('./preferences/user_name.txt') as user_name_file:
	global user_name
	user_name = user_name_file.read().rstrip()

# <--- Unit Methods --->
# return first line of a generic greeting
def generate_generic_greeting_1():
	generic = []
	generic.append("Hello, " + user_name + ",")
	generic.append("Hello,")
	generic.append("Hi, there, " + user_name + ",")
	generic.append("Hi, there,")
	generic.append("Sup,")

	return random.choice(generic) 
# return the first line of a morning greeting
def generate_morning_greeting_1():
	morning = []
	morning.append("Good morning, " + user_name + ",")
	morning.append("Good morning,")
	morning.append("Top of the morning to ya,")

	return random.choice(morning)
# return the first line of an afternoon greeting
def generate_afternoon_greeting_1():
	afternoon = []
	afternoon.append("Good afternoon, " + user_name + ",")
	afternoon.append("Good afternoon,")

	return random.choice(afternoon) 
# return the first line of an evening greeting
def generate_evening_greeting_1():
	evening = []
	evening.append("Good evening, " + user_name + ",")
	evening.append("Good evening,")

	return random.choice(evening)
# return the first line of a night greeting
def generate_night_greeting_1():
	night = []
	night.append("Still at it, " + user_name + "?")
	night.append("Still at it?")

	return random.choice(night)
# return the second line of a generic greeting
def generate_generic_greeting_2():
    generic = []
    generic.append("How are you doing?")
    generic.append("What can I do for you?")
    generic.append("How can I help?")
    generic.append("Let me know if there is anything you need.")
    generic.append("What do you need?")
    generic.append("How may I assist you?")
    generic.append("What do you want?")
    generic.append("Are you about done then?")
    generic.append("What brings you my way?")
    generic.append("What can I do ya for?")
    generic.append("You rang?")

    return random.choice(generic)
# return a single-line signoff
def generate_generic_signoff():
    generic = []
    generic.append("Goodbye, let me know if you need anything else.")
    generic.append("Bon Voyage")
    generic.append("Until next time.")
    generic.append("Goodbye.")
    generic.append("Later.")
    generic.append("Have a good one.")
    generic.append("Chow.")
    generic.append("Farewell for now.")
    generic.append("Thank you and goodbye.")

    return random.choice(generic)

# <--- Core Methods --->
# returns the first line of a greeting, may be time-dynamic
def greeting_1():
	# decide if generic or tod greeting
	greet_types = ["generic", "tod"]
	greet_type = random.choice(greet_types)

	# return appropriate greeting
	if greet_type is "generic":
		output = generate_generic_greeting_1()
	else:
		current_hour = datetime.now().hour
		if current_hour > 4 and current_hour < 12:
			output = generate_morning_greeting_1()
		elif current_hour > 11 and current_hour < 16:
			output = generate_afternoon_greeting_1()
		elif current_hour > 15 and current_hour < 20:
			output = generate_evening_greeting_1()
		else:
			output = generate_night_greeting_1()

	return output
# return the second line of a greeting (redundant)
def greeting_2():
    output = generate_generic_greeting_2()
    return output
# return a single-line signoff (redundant)
def signoff():
	output = generate_generic_signoff()
	return output