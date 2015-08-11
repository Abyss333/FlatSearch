import urllib2, re, os, sys


applicantName = "Armin Schaare und Kai Korpi"

contactedFile = "contacted.txt"
"""str: Name of the file containing the IDs of all contacted flats"""
contacted = {}


applicationFile = "application.txt"
"""str: Name of the file containing the application"""
application = ""

blacklistFile = "blacklist.txt"
"""str: Name of the file containing all regex prohibiting contact in case of a match"""
blacklist = {}

whitelistFile = "whitelist.txt"
"""str: Name of the file containing all regex encouraging cantact in case of a match"""
whitelist = {}

class FlatOffer(object):
	"""Class representing a scanned flat offer with all its information

	Attributes:
		iden (str): Identification number of the offer.
		title (str): Title of the offer.
		address (str): Renter specified address.
		district (str): District where the flat is located.
		zipCode (str): ZIP Code.
		city (str): The city in which the flat is located.
		company (str): The offering company (can be n/a).
		contactName (str): The name of the contact person to use for an application (can be n/a).
		coldRent (str): Cold Rent per month.
		livingSpace (str): Size of the flat (in m^2)
		roomCount (str): Number of rooms

	"""

	def __init__(self, iden, title, address, district, zipCode, city, company, contactName, coldRent, livingSpace, roomCount):
		"""Constructor

		Args:
			iden (str): Identification number of the offer.
			title (str): Title of the offer.
			address (str): Renter specified address.
			district (str): District where the flat is located.
			zipCode (str): ZIP Code.
			city (str): The city in which the flat is located.
			company (str): The offering company (can be n/a).
			contactName (str): The name of the contact person to use for an application (can be n/a).
			coldRent (str): Cold Rent per month.
			livingSpace (str): Size of the flat (in m^2)
			roomCount (str): Number of rooms

		"""
		self.iden = iden
		self.title = title
		self.address = address
		self.district = district
		self.zipCode = zipCode
		self.city = city
		self.company = company
		self.contactName = contactName
		self.coldRent = coldRent
		self.livingSpace = livingSpace
		self.roomCount = roomCount


	def contact(self):
		"""Contacts the offerer with the specified application string
		"""

		#TODO: Contact offerer

		self.saveID()


	def saveID(self):
		"""Saves the ID to the specified file
		"""

		f = open(contactedFile, "a")
		f.write(self.iden + "\n")
		f.close


	def toString(self):
		"""Formats all important information of this offer into a string

		Returns:
			str: The formatted string.

		"""

		return "\nID:\t\t" + self.iden + "\nTitle:\t\t" + self.title + "\nAddress:\t" + self.address + "\n\t\t" + self.district + "\n\t\t" + self.zipCode + ", " + self.city + "\nCompany:\t" + self.company + "\nContact:\t" + self.contactName + "\nCold Rent:\t" + self.coldRent + "\nLiving Space:\t" + self.livingSpace + "\nRooms:\t\t" + self.roomCount

def search(regex, string, group=1):
	"""Searches the string for the regex and returns the specified group

	Args:
		regex (str): Regular Expression to match
		string (str): The string to search
		group(Optional[int]): The group of the match to return.

	Returns:
		str: The group of the matched string. Will be 'n/a' if no match or group index is invalid.

	"""

	result = ""
	try:
		result = re.search(regex, string).group(group)
	except:
		result = "n/a"
	return result

def loadContacted():
	"""Loads the 'contactedFile'.

	Returns:
		set: All seperated lines in the file.

	"""

	l = []

	if os.path.isfile(contactedFile):
		with open(contactedFile, "r") as f:
			l = f.read().split("\n")
			l = l[:len(l)-2]

	return set(l)
def loadApplication():
	"""Loads the 'applicationFile'.

	Note:
		Content of the 'applicationFile' can have following Variables:
			$(applicant) : The applicant (usually your name)
			$(greeting) : The greeting of the contact (prompt will ask the user for it)

	Returns:
		str: The application string.

	"""
	l = ""
	try:
		with open(applicationFile, "r") as f:
			l = f.read()
	except IOError as e:
		print "Application file error:", e
		sys.exit(1)

	l = l.replace('$(greeting)', 'Sehr geehrter Herr Arsch')
	l = l.replace('$(applicant)', applicantName)

	return l


def loadBlacklist():
	"""Loads the 'blacklistFile'

	Note:
		Content of the 'blacklistFile' should be formatted like so:

			districts dist1 dist2 dist3 ...
			cities city1 city2 city3 ...
			title t1 t2 t3 t4 ...
			...

		The order of those properties is not important.
		Properties of flat offers will be matched against those specified regex and will only be
		contacted if there was no match.

		Regex present in both, whitelist and blacklist, will be ignored. Essentially having the same 
		effect as if the regex is in neither of the files.

	Returns:
		hashtable: Hashtable with flat properties (such as 'districts', 'cities', titles', etc...) as keys an sets of regex as values

	"""

	l = []
	result = {}


	if os.path.isfile(blacklistFile):
		with open(blacklistFile, "r") as f:
			l = f.read().split("\n")
			l = l[:len(l)-2]

		for elem in l:
			spl = elem.split(" ")
			result[spl[0]] = set(spl[1:])

	return result
def loadWhitelist():
	"""Loads the 'whitelistFile'

	Note:
		Content of the 'whitelistFile' should be formatted exactly like the content of 'blacklistFile'

			districts dist1 dist2 dist3 ...
			cities city1 city2 city3 ...
			title t1 t2 t3 t4 ...
			...

		Regex present in both, whitelist and blacklist, will be ignored. Essentially having the same 
		effect as if the regex is in neither of the files.

	Returns:
		hashtable: Hashtable with flat properties (such as 'districts', 'cities', titles', etc...) as keys an sets of regex as values

	"""

	l = []
	result = {}

	if os.path.isfile(blacklistFile):
		with open(blacklistFile, "r") as f:
			l = f.read().split("\n")
			l = l[:len(l)-2]

		for elem in l:
			spl = elem.split(" ")
			result[spl[0]] = set(spl[1:])

	return result

def findFlatsImmoscout24(maxColdRent, minRoomCount):
	"""Finds all flats on the website 'http//www.immobilienscout24.de/' with the given attributes.

	Args:
		maxColdRent(int): The maximum rent of the flat in Euro.
		minRoomCount(int): The minimum number of rooms of the flat.

	Returns:
		[FlatOffers]: The list of all search results.
	
	"""

	print "\nScanning Webpage http://www.immobilienscout24.de/ with a maximum rent of " + str(maxColdRent) + ",00EURO and a minimum room count of " + str(minRoomCount) + "."

	s = urllib2.urlopen('http://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Hamburg/Hamburg/-/' + str(minRoomCount) + ',00-/-/EURO--' + str(maxColdRent) + ',00?pagerReporting=true').read()

	flats = []

	n = int(search('numberOfHits: (.*?),', s)) / 20

	for a in range(1):
		
		print('\nScanning page ' + str(a + 1) + '...')

		s = urllib2.urlopen('http://www.immobilienscout24.de/Suche/S-T/P-' + str(a + 1) + '/Wohnung-Miete/Hamburg/Hamburg/-/' + str(minRoomCount) + ',00-/-/EURO--' + str(maxColdRent) + ',00?enteredFrom=one_step_search').read()

		m = re.finditer('\{\"id\":.*?\"similarResults\":\[.*?\]\}', s)

		for i in m:

			s = i.group(0)

			iden = search('\"id\":(.*?),', s)

			if iden not in contacted:

				title = search('\"title\":\"(.*?)\"', s)
				address = search('\"address\":\"(.*?)\"', s)
				district = search('\"district\":\"(.*?)\"', s)
				city = search('\"city\":\"(.*?)\"', s)
				zipCode = search('\"zip\":\"(.*?)\"', s)
				company = search('\"realtorCompanyName\":\"(.*?)\"', s)
				contactName = search('\"contactName\":\"(.*?)\"', s)
				coldRent = search('\"Kaltmiete\",\"value\":\"(.*?)\"', s)
				livingSpace = search('che\",\"value\":\"(.*?)\"', s)
				zimmer = search('\"Zimmer\",\"value\":\"(.*?)\"', s)

				flat =  FlatOffer(iden, title, address, district, zipCode, city, company, contactName, coldRent, livingSpace, zimmer)
				flats.append(flat)
				print(flat.toString())

	return flats

def main():
	"""Main method to commence a flat search
	"""

	os.remove(contactedFile)

	contacted = loadContacted()
	application = loadApplication()
	blacklist = loadBlacklist()
	whitelist = loadWhitelist()

	print(application)

	flats = findFlatsImmoscout24(500, 2)	

	for f in flats:
		f.contact()

if __name__ == "__main__":

	main()

#http://www.immobilienscout24.de/Suche/S-T/P-1/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?enteredFrom=one_step_search
#http://www.immobilienscout24.de/Suche/S-T/P-2/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?pagerReporting=true
#http://www.immobilienscout24.de/expose/83076908?referrer=RESULT_LIST_LISTING&navigationServiceUrl=%2FSuche%2Fcontroller%2FexposeNavigation%2Fnavigate.go%3FsearchUrl%3D%2FSuche%2FS-T%2FWohnung-Miete%2FHamburg%2FHamburg%2F-%2F2%2C00-%2F-%2FEURO--500%2C00%26exposeId%3D83076908&navigationHasPrev=true&navigationHasNext=true&navigationBarType=RESULT_LIST&searchId=44cfea78-3276-3a5f-9680-db6f8e4cc27b