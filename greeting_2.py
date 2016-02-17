#!/usr/bin/env python
import random

# create array of possible generic grettings
def generate_generic_greeting():
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

    return random.choice(generic)

def main():
    output = generate_generic_greeting()
    return output

if __name__ == '__main__':
    main()
