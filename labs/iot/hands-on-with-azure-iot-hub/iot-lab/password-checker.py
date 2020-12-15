import re 
import sys

password=sys.argv[1]

matches=0

if len(password) < 12:
	print('ERROR: Password length must be greater than 11 characters')
	sys.exit(1)

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
	
if (any(x.isupper() for x in password)):
	matches += 1

if (any(x.islower() for x in password)):
	matches += 1

if (any(x.isdigit() for x in password)):
	matches += 1
	
if(regex.search(password) != None): 
    matches += 1
	
if matches < 3:
	print('ERROR: Password must contain 3 of the following. A special character, an uppercase, a lowercase and a digit')
	sys.exit(1)