import re 
import sys

group = sys.argv[1]

if len(group) < 2:
	sys.exit(1)

if group[-1] not in ['c', 'h']:
	sys.exit(1)

if len(group) == 2:
	group = "0"+group

print(group)