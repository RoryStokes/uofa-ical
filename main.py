import icalendar,pytz,datetime
import myparser,subject,exporter

inPath  = raw_input("Enter the (relative) path to the HTML file you wish to convert: ")
outPath = raw_input("Enter the (relative) path to store the output ICS file (*.ics): ")

inFile  = open(inPath ,"r")
outFile = open(outPath,"w")

# create a subclass and override the handler methods


# instantiate the parser and fed it some HTML
p = myparser.Parser()
p.feed(inFile.read())
inFile.close()

e = exporter.Exporter()

for subject in p.subjects:
	for event in subject.events:
		e.addEvent(subject,event)

outFile.write(e.to_ical())
outFile.close

print "Success! Written to ",outPath
exit = raw_input("Press enter to exit")