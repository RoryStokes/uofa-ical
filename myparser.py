from HTMLParser import HTMLParser
import subject

class Parser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.reading        = False
		self.readData       = False
		self.currentSubject = None
		self.targetFunction = None
		self.eventCount     = 0
		self.eventType      = ""
		self.eventDates     = ""
		self.eventDay       = ""
		self.eventTimes     = ""
		self.eventLocation  = ""
		self.subjects       = []
		self.rooms          = {}
		self.currentCol     = 0
		self.topicSpan      = 0
		self.typeSpan       = 0

	def read_data(self,target):
		self.targetFunction = target
		self.readData = True

	def setEventType(self,data):
		self.eventType = data
	def setEventDates(self,data):
		self.eventDates = data
	def setEventDay(self,data):
		self.eventDay = data
	def setEventTimes(self,data):
		self.eventTimes = data
	def setEventLocation(self,data):
		if data in self.rooms:
			self.eventLocation = self.rooms[data]
		else:
			done = False

			while not done:
				tempName = raw_input("New room '"+data+"' found for "+self.currentSubject.name+" "+self.eventType+", nickname? (leave blank to keep existing name): ")

				if tempName == "":
					self.eventLocation = data
					self.rooms[data] = data
					done = True
				else:
					check = raw_input("Naming subject '"+tempName+"' are you sure (Y/n): ")
					while check not in "yYnN":
						check = raw_input("Please choose (Y/n):")
					if check in "yY":
						self.eventLocation = tempName
						self.rooms[data] = tempName
						done = True
		self.addEvent()

	def addEvent(self):
		self.currentSubject.addEvent(self.eventType, self.eventDates, self.eventDay, self.eventTimes, self.eventLocation)


	def handle_starttag(self, tag, attrs):
		attrs = dict(attrs)
		if self.reading:
			if tag == "td":
				self.currentCol += 1
				if self.currentCol == 1:
		 			if "rowspan" in attrs and not self.eventCount:
		 				#NEW SUBJECT
						self.currentSubject = subject.Subject()
		 				self.subjects.append(self.currentSubject)
						self.eventCount     = int(attrs['rowspan'])
						self.topicSpan      = int(attrs['rowspan'])-1
				elif self.currentCol == 3:
					self.read_data(self.setEventType)
					if 'rowspan' in attrs:
						self.typeSpan = int(attrs['rowspan'])-1
				elif self.currentCol == 4:
					self.read_data(self.setEventDates)
				elif self.currentCol == 5:
					self.read_data(self.setEventDay)
				elif self.currentCol == 6:
					self.read_data(self.setEventTimes)
				elif self.currentCol == 7:
					self.read_data(self.setEventLocation)
			elif tag == "br":
				if not self.currentSubject.name and self.currentCol == 1:
					self.read_data(self.currentSubject.loadName)
			elif tag == "tr":
				self.currentCol = 0
				if self.topicSpan:
					self.currentCol += 1
				if self.typeSpan:
					self.currentCol += 2

				if self.eventCount:
					self.eventCount -= 1
					self.topicSpan  -= 1
				if self.typeSpan:
					self.typeSpan   -= 1

		if tag == "table" and 'cellpadding' in attrs:
			if attrs['cellpadding'] == "3":
				self.reading = True

	def handle_endtag(self, tag):
		if "table" in tag:
			self.reading = False

	def handle_data(self, data):
		if self.readData:
			#print self.targetFunction
			self.targetFunction(data)
			self.readData = False