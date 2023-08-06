import smtplib
from email.message import EmailMessage
import os
import pickle
import imghdr
import json

class Gmail():
	def __init__(self, email=None, password=None):
		self.addr = email
		self.Pass = password
		self.s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		self.msg = EmailMessage()

	def register(self, name):
		'''This is where you register'''
		data = {}
		data["addr"] = self.addr
		data["pass"] = self.Pass
		path = os.path.join(os.getcwd(), "registers")
		name = name + ".pickle"
		if os.path.isdir(path):
			f = open(os.path.join(path, name), "wb")
			pickle.dump(data, f)
			f.close()

		else:
			os.mkdir(path)
			f = open(os.path.join(path, name), "wb")
			pickle.dump(data, f)
			f.close()

	def load(self, name):
		'''This is where you load'''
		name = name + ".pickle"
		path = os.path.join(os.getcwd(), "registers", name)
		dirs = os.listdir(os.path.split(path)[0])
		try:
			f = open(path, "rb")
			data = pickle.load(f)
			f.close()
			self.addr = data["addr"]
			self.Pass = data["pass"]
		except FileNotFoundError:
			name = name.replace(".pickle", "")
			raise Exception(f"The Name {name} was not registered")

	def memberList(self):
		'''This is where you get the list of registered members'''
		path = os.path.join(os.getcwd(), "registers")
		lista = os.listdir(path)
		listmem = []
		for i in lista:
			listmem.append(os.path.splitext(i)[0])
		return listmem

	def setMessage(self, subject, to):
		'''This is where you Set Message'''
		self.msg['Subject'] = subject
		self.msg['From'] = self.addr
		self.msg['To'] = to

	def setContent(self, content):
		'''This is where you Set Message Content'''
		self.msg.set_content(content)

	def addAttachment(self, path:list, types:list):
		'''This is where you Add Attachment'''
		fd = open("types.json", "r")
		fdata = dict(json.loads(fd.read()))
		fd.close()
		typea = []
		for i in types:
			if i.isupper():
				typea.insert(types.index(i), i)
			elif i.islower():
				typea.insert(types.index(i), i.upper())
		types = typea
		for i, j in zip(path, types):
			f = open(i, "rb")
			fd = f.read()
			fn = f.name
			if fdata[j]["id"] == "Nan":
				fdata[j]["id"] = imghdr.what(fn)

			self.msg.add_attachment(fd, maintype=fdata[j]["type"], subtype=fdata[j]["id"], filename=fn)

	def addHTML(self, path):
		'''This is where you Add HTML'''
		with open(path, 'rb') as f:
		    file_data = f.read()
		    file_type = imghdr.what(f.name)
		    file_name = f.name

		file_string = file_data.decode(encoding='UTF-8')

		self.msg.add_alternative(file_string, subtype='html')

	def login(self):
		'''This is where you Login'''
		self.s.login(self.addr, self.Pass)

	def sendMessage(self):
		'''Well obiviously send message'''
		self.s.send_message(msg=self.msg)
