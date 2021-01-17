import json

class Parser:
	"""
	class to Parse Json file
	"""
	def __init__(self, filename):
		with open(filename) as json_file:
			data = json.load(json_file)
		self.data = data["program"]["body"]

	def getData(self):
		return self.data

	def display(self):
		"""
		"""
		print(self.getData())

