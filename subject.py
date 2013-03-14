import event

class Subject:
	def __init__(self):
		self.name = None
		self.events = []

	def loadName(self,name):
		done = False

		while not done:
			tempName = raw_input("Nickname for subject '"+name+"''? (leave blank to keep existing name): ")
			if tempName == "":
				self.name = name
				done = True
			else:
				check = raw_input("Naming subject '"+tempName+"', are you sure (Y/n): ")
				while check not in "yYnN":
					check = raw_input("Please choose (Y/n):")
				if check in "yY":
					self.name = tempName
					done = True

	def addEvent(self, *params):
		self.events.append(event.Event(*params))