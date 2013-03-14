import icalendar,pytz,datetime
import event
from dateutil.rrule import *

class Exporter(icalendar.Calendar):
	def __init__(self):
		icalendar.Calendar.__init__(self)

		self.add('prodid', '-//Adelaid Uni Auto iCalendar//Rory Stokes//')
		self.add('version', '2.0')
		self.add('x-wr-timezone', u"Australia/Adelaide")

		self.add('x-wr-calname', u"University Timetable")
		self.add('x-wr-caldesc', u"Automatically Generated UofA Timetable")

		tzc = icalendar.Timezone()
		tzc.add('tzid', 'Australia/Adelaide')
		tzc.add('x-lic-location', 'Australia/Adelaide')

		tzs = icalendar.TimezoneStandard()
		tzs.add('tzname', 'CST')
		tzs.add('dtstart', datetime.datetime(1970, 10, 25, 3, 0, 0))
		tzs.add('rrule', {'freq': 'yearly', 'bymonth': 4, 'byday': '1su'})
		tzs.add('TZOFFSETFROM', datetime.timedelta(hours=10,minutes=30))
		tzs.add('TZOFFSETTO', datetime.timedelta(hours=9,minutes=30))

		tzd = icalendar.TimezoneDaylight()
		tzd.add('tzname', 'CST')
		tzd.add('dtstart', datetime.datetime(1970, 3, 29, 2, 0, 0))
		tzs.add('rrule', {'freq': 'yearly', 'bymonth': 10, 'byday': '1su'})
		tzd.add('TZOFFSETFROM', datetime.timedelta(hours=9,minutes=30))
		tzd.add('TZOFFSETTO', datetime.timedelta(hours=10,minutes=30))

		tzc.add_component(tzs)
		tzc.add_component(tzd)
		self.add_component(tzc)

	def addEvent(self,subject,event):
		temp = icalendar.Event()
		tz = pytz.timezone("Australia/Adelaide")
		d = datetime.datetime
		temp.add('dtstart', event.startTime)
		temp.add('dtend',  event.endTime)
		temp.add('dtstamp', d.now(tz))
		temp.add('created', d.now(tz))
		#event.add('uid', u'123456')
		temp.add('last-modified', d.now(tz))
		temp.add('summary', subject.name+" "+event.type)
		if event.untilTime:
			temp.add('rrule', {'freq': 'weekly', 'until': event.untilTime})
		temp.add('description', '')
		temp.add('location', event.location)
		self.add_component(temp)