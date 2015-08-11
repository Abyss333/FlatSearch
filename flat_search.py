import urllib2, re, os



class Flat(object):

	contacted = "contacted.txt"

	def __init__(self, iden, title, address, district, zipCode, city, company, contactName, coldRent, livingSpace, roomCount):

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

		if len(self.company) > 500:
			self.company = re.search("(^.*?)\"", self.company).group(1)
			self.contactName = "K.A."

		self.saveID()

	def saveID(self):
		f = open(Flat.contacted, "a")
		f.write(self.iden + "\n")
		f.close

	def toString(self):

		return "\nID:\t\t" + self.iden + "\nTitle:\t\t" + self.title + "\nAddress:\t" + self.address + "\n\t\t" + self.district + "\n\t\t" + self.zipCode + ", " + self.city + "\nCompany:\t" + self.company + "\nContact:\t" + self.contactName + "\nCold Rent:\t" + self.coldRent + "\nLiving Space:\t" + self.livingSpace + "\nRooms:\t\t" + self.roomCount

def search(regex, string):
	result = ""
	try:
		result = re.search(regex, string).group(1)
	except:
		result = "n/a"
	return result


if __name__ == "__main__":

	os.remove(Flat.contacted)

	contIDs = []

	if os.path.isfile(Flat.contacted):
		with open(Flat.contacted, "r") as f:
			contIDs = f.read().split("\n")
			contIDs = contIDs[:len(contIDs)-2]

	#with open("konaktierte.txt")

	
	#m = re.finditer('((?<=CompanyName":).{1500})', r.read())

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

				flat =  Flat(iden, title, address, district, zipCode, city, company, contactName, coldRent, livingSpace, zimmer)
				flats.append(flat)
				print(flat.toString())

	#http://www.immobilienscout24.de/Suche/S-T/P-1/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?enteredFrom=one_step_search
	#http://www.immobilienscout24.de/Suche/S-T/P-2/Wohnung-Miete/Hamburg/Hamburg/-/2,00-/-/EURO--500,00?pagerReporting=true
	#http://www.immobilienscout24.de/expose/83076908?referrer=RESULT_LIST_LISTING&navigationServiceUrl=%2FSuche%2Fcontroller%2FexposeNavigation%2Fnavigate.go%3FsearchUrl%3D%2FSuche%2FS-T%2FWohnung-Miete%2FHamburg%2FHamburg%2F-%2F2%2C00-%2F-%2FEURO--500%2C00%26exposeId%3D83076908&navigationHasPrev=true&navigationHasNext=true&navigationBarType=RESULT_LIST&searchId=44cfea78-3276-3a5f-9680-db6f8e4cc27b