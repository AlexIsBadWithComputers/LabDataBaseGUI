from ColumnHeaders import Headers, Exceptions
import os 
import re

class IsotopeData():
	"""
	This class will be used to extract the ratios (and sometimes intensities)
	of isotope data from the ASCII grid exports of the Thermo software. Using
	this class, it will see what element is being used and parse the data 
	accordingly.
	"""
	def __init__(self,ElementOfChoice):
		"""
		Grab column headers from a dictionary supplied in ColumnHeaders
		"""
		
		self.Heads =  Headers[ElementOfChoice]


		# first, the Spacing between elements for the Thermo files is a tab, so:
		self.BreakChar = "	"
		#print(self.Heads)

	def GrabData(self,file):
		"""
		Search for data in supplied file to extract. All
		This requires is the file name, as well as the column headers that
		it is looking for.
		"""
		f = open(file, 'r')
		mydate = None

		# Search through the file for the data we want.
		
		for lines in f.readlines():
			
			if "Cycle" in lines:
				self.MakeIndicies(lines)
				
			if "***	Mean" in lines:
				grab = lines.split(self.BreakChar)
				data = [None for i in range(len(self.Heads))]

				# Control the order of things and fill NULL for files formatted unexpecdedly
				# This works because I've filled the "header" dictionary using the actual
				# Data file. So if it's missing something we expect, It's easier just 
				# to say it's NULL. Plus, this way the files will exist in all tables,
				# even if they're full of NULL values. But this has the benefit that 
				# I'll at least catch some parts rather than ignoring the whole file.
				# I would also like to note this wouldn't be an issue if everyone would
				# just agree on a standard file format. But nooooooooooooo that would be
				# too difficult. I might be bitter.

				# TODO: Remove bitter comment above. 
				
				for headers in self.Heads:
					try:
						data[self.Heads.index(headers)] =  grab[self.IndexDict[headers]]
					except KeyError:
						data[self.Heads.index(headers)] = None
						continue

			if "***	StdErr (abs)" in lines:
				grab = lines.split(self.BreakChar)
				errors = [None for i in range(len(self.Heads))]

				for headers in self.IndexDict:
					try:
						errors[self.Heads.index(headers)] =  grab[self.IndexDict[headers]]
					except KeyError:
						errors[self.Heads.index(headers)] = None
						continue
			
			if "date" in lines:
				
				date = lines.split()	
				date = date[2].split(os.sep)
				if len(str(date[0])) < 2:
					date[0] = '0' + str(date[0])
				if len(str(date[1])) < 2:
					date[1] = '0' + str(date[1])
				mydate = str('{}{}{}{}{}'.format(date[2],"-",date[0],"-",date[1]))

		f.close()
		# Return the data we yoinked from files. 
		try:
			return data, errors, mydate
		# Probably won't hit this, but It might fill it like this anyways 	
		except NameError:
			data = [None for i in range(len(self.Heads))]
			errors = [None for i in range(len(self.Heads))]
			mydate = None


	def MakeIndicies(self,line):
		"""
		This function takes a line of interest and finds the indexes of our column headers 
		for the data we're extracting
		"""
		BrokenLine = line.split(self.BreakChar)
		self.IndexDict = {}

		for i, LineStuff in enumerate(BrokenLine):
			for head in self.Heads:
				if Exceptions.has_key(head):
					regex = Exceptions[head]
				else:
					regex = r'(\s|^|$)' + head + r'(\s|^|$)'
				match = re.search(regex, LineStuff)
				if match:
					# Prevents overwriting of a key if an intensity 
					# has been hit as a ratio. Basically this protects
					# us from my laziness from if head in linestuff.

					if self.IndexDict.has_key(head):
						pass
					else:
						self.IndexDict.update({head:i})








