#!/usr/bin/env python
### BEGIN LICENSE
# Copyright (C) 2016 Peter <peter.nfonseca@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE
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

from rvsdata import user_name

# <--- Unit Methods --->
# return first line of a generic greeting
def generate_generic_greeting_1():
  generic = [
    "Hello, " + user_name + ",",
    "Hello,",
    "Hi there, " + user_name + ",",
    "Hi there,",
    "Sup,"
  ]
  return random.choice(generic) 

# return the first line of a morning greeting
def generate_morning_greeting_1():
  morning = [
    "Good morning, " + user_name + ",",
    "Good morning,",
    "Top of the morning to ya,"
  ]
  return random.choice(morning)

# return the first line of an afternoon greeting
def generate_afternoon_greeting_1():
  afternoon = [
    "Good afternoon, " + user_name + ",",
    "Good afternoon,"
  ]
  return random.choice(afternoon) 

# return the first line of an evening greeting
def generate_evening_greeting_1():
  evening = [
    "Good evening, " + user_name + ",",
    "Good evening,"
  ]
  return random.choice(evening)

# return the first line of a night greeting
def generate_night_greeting_1():
  night = [
    "Still at it, " + user_name + "?",
    "Still at it?"
  ]
  return random.choice(night)

# return the second line of a generic greeting
def generate_generic_greeting_2():
  generic = [
    "How are you doing?",
    "What can I do for you?",
    "How can I help?",
    "What can I help you with?",
    "Let me know if there is anything you need.",
    "What do you need?",
    "How may I assist you?",
    "What brings you my way?",
    "What can I do ya for?",
    "You rang?"
  ]
  return random.choice(generic)

# return a single-line signoff
def generate_generic_signoff():
  generic = [
    "Goodbye, let me know if you need anything else.",
    "Bon Voyage",
    "Until next time.",
    "Goodbye.",
    "Later.",
    "Have a good one.",
    "Chow.",
    "Farewell for now.",
    "Thank you and goodbye."
  ]
  return random.choice(generic)

# return a single-line your welcome
def generate_generic_yourewelcome():
  generic = [
    "You're welcome.",
    "You're quite welcome.",
    "It's my pleasure.",
    "No, thank you.",
    "No problem.",
    "Any time.",
    "No need to thank me, it's my job",
    "Prego."
  ]
  return random.choice(generic)

# return a single-line thanks
def generate_generic_thankyou():
  generic = [
    "Thank you.",
    "Why thank you.",
    "Much appreciated",
    "You don't say.",
    "Grazie."
  ]
  return random.choice(generic)

# return a single-line response to an unrecognized input
def generate_generic_reponse():
  generic = [
    "Could you phrase that a different way?",
    "Excuse me, I didn't quite get that.",
    "Whuh?",
    "Excuse me?",
    "I beg your pardon.",
    "Come again?",
    "Does not compute.",
    "Anecdote accepted. Snappy comeback not found."
  ]
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

# return a single-line you're welcome (redundant)
def yourewelcome():
  output = generate_generic_yourewelcome()
  return output

# return a single-line thank you (redundant)
def thankyou():
  output = generate_generic_thankyou()
  return output

# return a generic response to an unknown input (redundant)
def response():
  output = generate_generic_reponse()
  return output

# return a single-line signoff (redundant)
def signoff():
  output = generate_generic_signoff()
  return output
