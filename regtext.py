import re

# Put the column header you want to test here
string = '58.855/57Fe'

# Now, test your regular expression. 
stuff=re.search('\d+\.\d+/57Fe',string)


# If this prints "Nailed it", feel free to add your regular expression and key
# to the exceptions dictionary. 
if stuff:
	print("Nailed it")
else:
	print("Nope")