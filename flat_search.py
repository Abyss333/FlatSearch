import urllib2, re, os

contactedFile = "contacted.txt"
"""str: Name of the file containing the IDs of all contacted flats"""

applicationFile = "application.txt"
"""str: Name of the file containing the application"""

blacklistFile = "blacklist.txt"
"""str: Name of the file containing all regex prohibiting contact in case of a match"""

whitelistFile = "whitelist.txt"
"""str: Name of the file containing all regex encouraging cantact in case of a match"""

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
		livingSpace (str): Size of the flat (in m²)
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
			livingSpace (str): Size of the flat (in m²)
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

		f = open(FlatOffer.contacted, "a")
		f.write(self.iden + "\n")
		f.close


	def toString(self):
		"""Formats all importent information of this offer into a string

		Returns:
			str: The formatted string.

		"""

		return "\nID:\t\t" + self.iden + "\nTitle:\t\t" + self.title + "\nAddress:\t" + self.address + "\n\t\t" + self.district + "\n\t\t" + self.zipCode + ", " + self.city + "\nCompany:\t" + self.company + "\nContact:\t" + self.contactName + "\nCold Rent:\t" + self.coldRent + "\nLiving Space:\t" + self.livingSpace + "\nRooms:\t\t" + self.roomCount


def search(regex, string, group=0):
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
	"""Loads the 'contactedFile' containing all ID of already contacted offers.

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

	Returns:
		str: All seperated lines in the file.

	"""

	l = []

	if os.path.isfile(contactedFile):
		with open(contactedFile, "r") as f:
			l = f.read().split("\n")
			l = l[:len(l)-2]

	return set(l)


def main():
	"""Main method to commence a flat search
	"""

	os.remove(contacted)

	contacted = loadContacted()



	s = urllib2.urlopen('http://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?pagerReporting=true').read()

	flats = []

	n = int(re.search('numberOfHits: (.*?),', s).group(1)) / 20

	for a in range(n):
		
		print('\nScanning page ' + str(a + 1) + '...')

		s = urllib2.urlopen('http://www.immobilienscout24.de/Suche/S-T/P-' + str(a + 1) + '/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?enteredFrom=one_step_search').read()

		m = re.finditer('\{\"id\":.*?\"similarResults\":\[.*?\]\}', s)

		#m = re.finditer('\"id\":(.*?),\".*?\"title\":\"(.*?)\",\"address\":\"(.*?)\",\"district\":\"(.*?)\",\"city\":\"(.*?)\",\"zip\":\"(.*?)\".*?\"realtorCompanyName\":\"(.*?)\",\"contactName\":\"(.*?)\".*?\"value\":\"(.*?)\".*?\"value\":\"(.*?)\".*?\"value\":\"(.*?)\"', s)

		for i in m:

			s = i.group(0)

			iden = search('\"id\":(.*?),', s)

			if iden not in contIDs:

				title = search('\"title\":\"(.*?)\"', s, 1)
				address = search('\"address\":\"(.*?)\"', s, 1)
				district = search('\"district\":\"(.*?)\"', s, 1)
				city = search('\"city\":\"(.*?)\"', s, 1)
				zipCode = search('\"zip\":\"(.*?)\"', s, 1)
				company = search('\"realtorCompanyName\":\"(.*?)\"', s, 1)
				contactName = search('\"contactName\":\"(.*?)\"', s, 1)
				coldRent = search('\"Kaltmiete\",\"value\":\"(.*?)\"', s, 1)
				livingSpace = search('che\",\"value\":\"(.*?)\"', s, 1)
				zimmer = search('\"Zimmer\",\"value\":\"(.*?)\"', s, 1)

				flat =  FlatOffer(iden, title, address, district, zipCode, city, company, contactName, coldRent, livingSpace, zimmer)
				flats.append(flat)
				print(flat.toString())


if __name__ == "__main__":

	main()



#http://www.immobilienscout24.de/Suche/S-T/P-1/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?enteredFrom=one_step_search
#http://www.immobilienscout24.de/Suche/S-T/P-2/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?pagerReporting=true
#http://www.immobilienscout24.de/expose/83076908?referrer=RESULT_LIST_LISTING&navigationServiceUrl=%2FSuche%2Fcontroller%2FexposeNavigation%2Fnavigate.go%3FsearchUrl%3D%2FSuche%2FS-T%2FWohnung-Miete%2FHamburg%2FHamburg%2F-%2F2%2C00-%2F-%2FEURO--500%2C00%26exposeId%3D83076908&navigationHasPrev=true&navigationHasNext=true&navigationBarType=RESULT_LIST&searchId=44cfea78-3276-3a5f-9680-db6f8e4cc27b