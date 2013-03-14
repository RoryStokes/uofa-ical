import pytz,datetime

class Event:
	def __init__(self,type,dates,day,times,location):
		self.type     = type
		self.location = location
		local = pytz.timezone('Australia/Adelaide')
		d = datetime.datetime
		dates  = dates.split(' - ')
		times  = times.split(' - ')
		format = '%d %b %Y %I:%M%p'

		startStr = dates[0]+" "+str(d.now().year)+" "+times[0]
		endStr   = dates[0]+" "+str(d.now().year)+" "+times[1]
		if len(dates) > 1:
			untilStr = dates[1]+" "+str(d.now().year)+" "+times[1]
			self.untilTime = d.strptime(untilStr, format)
		else:
			self.untilTime = None

		self.startTime = local.localize(d.strptime(startStr,format))
		self.endTime   = local.localize(d.strptime(endStr,  format))

