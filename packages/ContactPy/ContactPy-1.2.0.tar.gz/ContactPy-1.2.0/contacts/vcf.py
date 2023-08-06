class VCard():
	def __init__(self, filename:str):
		self.filename = filename

	def create(self, display_name:list, full_name:str, number:str, email:str=None):
		'''Create a vcf card'''
		bp = [1, 2, 0]
		pp = [0, 1, 2]
		rn = []
		for i, j in zip(bp, pp):
			rn.insert(i, display_name[j]+";")

		fd = self.filename
		f = open(fd, "w")
		f.write("BEGIN:VCARD\n")
		f.write("VERSION:2.1\n")
		f.write("N:")
		for i in rn:
			f.write("{}".format(i))
		f.write("\n")
		f.write("FN:{}\n".format(full_name))
		f.write("TEL;CELL;PREF:{}\n".format(number))
		f.write("EMAIL;HOME:{}\n".format(email))
		f.write("END:VCARD")
		f.close()

	def read(self, att:str):
		'''Read a card'''
		global name, full_name, number, email
		filenameWithDirectory = self.filename
		bp = [1, 2, 0]
		pp = [0, 1, 2]
		oriname = []
		nameind, fnind, phind, emind = None, None, None, None
		with open(filenameWithDirectory, 'r') as f:
			card = [line.strip() for line in f]
		for i in card:
			if "N:" in i:
				nameind = card.index(i)
			if "FN:" in i:
				fnind = card.index(i)
			if "TEL;CELL;PREF:" in i:
				phind = card.index(i)
			if "TEL;CELL:" in i:
				phind = card.index(i)
			if "EMAIL;HOME:" in i:
				emind = card.index(i)

		if nameind != None:
			name = card[fnind]
			name = name[2:len(name)]
			name = name.replace(":","")
			name = name[0:len(name)]
			namel = name.split(";")
		if fnind != None:
			full_name = card[nameind]
			full_name = full_name[3:len(full_name)]
		if phind != None:
			number = card[phind]
			try:
				number = str(number).replace("TEL;CELL:","")
				number = int(number)
			except:
				number = str(number).replace("TEL;CELL;PREF:","")
				number = int(number)
		if emind != None:
			email = card[emind]
			email = email[11:len(email)]
		elif emind == None:
			email = None

		info = {}
		infol = ["name", "full_name", "number", "email"]
		infola = [name, full_name, number, email]
		for i, j in zip(infol, infola):
			info[i] = j
		return info[att]

	@property
	def number(self):
		return self.read("number")

	@property
	def name(self):
		return self.read("name")

	@property
	def fullName(self):
		return self.read("full_name")

	@property
	def email(self):
		return self.read("email")