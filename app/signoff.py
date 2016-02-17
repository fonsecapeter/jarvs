#!/usr/bin/env python
import random

# create array of possible generic signoffs
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

def main():
	output = generate_generic_signoff()
	return output

if __name__ == '__main__':
    main()