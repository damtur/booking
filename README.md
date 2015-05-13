Api to create simple booking system based on csv file.

Task:
	This task is about a room booking micro-service to be exposed to clients over the Internet. It will be used to manage the meeting schedule in a busy office. It allows people to find existing bookings in a room, make a booking, and cancel a booking. The service will be consumed by a variety of clients.

	A previous version of the service has been in use for some time. The old data has been exported as an RFC 4180 compliant CSV file. Each line is a booking, containing the fields bookingId (an integer, unique among all bookings), roomId (an integer identifying the room being booked), bookerName (a string), startTime and endTime (both strings encoding an ISO 8601 datetime without a timezone, e.g. 1997-07-16T19:20). These field names are given as the first line in the file, as per section 2.3 of the RFC. The order of the fields is not known, and may change between files. The file may be large. You can assume that the bookings are all consistent; there are no invalid times, duplicate booking identifiers or overlapping bookings in the same room. The problem is broken down into the following tasks:

	1. Design and implement a model layer for the key elements of the system. The choice of elements is up to you, but you might want to consider entities such as Room and Person. 

	2. Create functionality to load a CSV file into a suitable structure, using your model where appropriate.

	3. Implement functionality to find the next available booking slot for a meeting, where “next” is calculated from 1st April 2015 at 00:00 GMT. This should take a duration (i.e. 3 hours), and return the next available room and time which can accommo- date it. Assume rooms can be used continuously (24 hours a day, all year around).

	4. Package the resulting code into a “Find next booking” program. It should take a path to a CSV file containing existing booking information, and the duration of the meeting in seconds. It 1 should output the room identifier and start time of the first available slot. For example, if you provide a command line application, the usage might be: $ yourApp ./example.csv 3600



Solution:

I have created a simple python application. I would now separate solution to multiple files, but I wanted to keep it simple for testing.

Usage:

run ./booking.py -h

(This will give you help)

Other possibilities:

./booking.py -i data/smallSet.csv -d 10800

You may use following parameters:
	-i = input file name (default is 'data/smallSet.csv')
	-d = duration in seconds (default is 3 hours so 10800)
	-h = this help
	-t = test run (will use data/smallSet.csv file and check next available booking slot function)