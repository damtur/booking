#!/usr/bin/python

import sys
import getopt
import csv
from datetime import timedelta, datetime


class Formatters(object):
	@staticmethod
	def fromUTC(utcTime, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
		""" Convert UTC time string to time.struct_time """
		# change datetime.datetime to time, return time.struct_time type
		return datetime.strptime(utcTime, fmt)

	@staticmethod
	def fromTimeWithTimezoneUTC(timeWithTimezone, fmt="%Y-%m-%d %H:%M:%S"):
		""" Convert UTC time string to time.struct_time """

		try:
			offset = int(timeWithTimezone[-5:])
		except:
			print "Error while trying to get timezone trying UTC date"
			return fromUTC(timeWithTimezone)

		delta = timedelta(hours=offset/100)
		time = datetime.strptime(timeWithTimezone[:-6], fmt)
		time -= delta

		return time


class Booking(object):
	""" Class representing one booking """

	def __init__(self, bookingId, client, room, startTime, endTime):
		self.bookingId = bookingId
		self.client = client
		self.room = room
		self.startTime = startTime
		self.endTime = endTime

class Person(object):
	""" Class representing booking people. So far it just have
		simple info such as personId, but it may be extended to
		contain address, contact data, email and so on """

	# Normally would be from database sequence
	lastPersonId = -1

	def __init__(self, name):
		self.personId = Person._getNextPersonId()
		self.name = name

	@staticmethod
	def _getNextPersonId():
		Person.lastPersonId += 1
		return Person.lastPersonId


class Room(object):
	""" Class representing a room. It may be extended by some 
	    properties like capacity, floor etc """

	def __init__(self, roomId):
		self.roomId = roomId
		# To store booking for that room for easier access
		self.bookings = {}


class Hotel(object):
	""" Main class for the hotel which keep track of all bookings,
		clients (Person) and Rooms """

	def __init__(self):
		self.bookings = []
		# Clients might be stored by Id, but for simplicity it will be by name
		# for now as search will be easier
		self.clientsByName = {}
		self.rooms = {}


	def loadFromFile(self, fileName):
		with open(fileName, mode='r') as bookingFile:
			reader = csv.DictReader(bookingFile)
			for booking in reader:
				self._addBooking(
					int(booking['bookingId']), 
					int(booking['roomId']),
					booking['bookerName'],
					Formatters.fromTimeWithTimezoneUTC(booking['startTime']),
					Formatters.fromTimeWithTimezoneUTC(booking['endTime']))


	def printBookings(self):
		print "Bookings:"
		for booking in self.bookings:
			print(str(booking.bookingId) + ", " + str(booking.startTime) + " - " + str(booking.endTime) + 
				" for " + booking.client.name + " in room " + str(booking.room.roomId))

	def printRooms(self):
		print "Rooms:"
		for room in self.rooms.itervalues():
			print room.roomId

	def printClients(self):
		print "Clients:"
		for clientName, client in self.clientsByName.iteritems():
			print str(client.personId) + ": " + client.name


	def findNextAvailableBookingSlot(self, duration=timedelta(hours=3), currentDate=datetime.strptime("2015-04-01 00:00", "%Y-%m-%d %H:%M")):
		if len(self.rooms) < 1: return (None, None)

		# Problem will be split to find next available time slot for each room individually and then return 
		# the soonest one. 
		roomsAvailabilityByStartTime = {}

		for room in self.rooms.itervalues():
			roomBookingsByStart = sorted(room.bookings.items(), key=lambda b: b[1].startTime)

			possibleStartTime = currentDate
			for startTime, booking in roomBookingsByStart:
				if booking.endTime < currentDate:
					continue
				if booking.startTime < currentDate:
					# we hit with date current booking move to end
					possibleStartTime = booking.endTime

				else:
					# next booking starts in future, check if we can fit before it
					if possibleStartTime + duration <= booking.startTime:
						if currentDate == possibleStartTime:
							# optimization we know that there are no sooner date so return room
							# as we just need one room
							return (currentDate, room)
						else:
							roomsAvailabilityByStartTime[possibleStartTime] = room
							break
					else:
						possibleStartTime = booking.endTime
						continue
			else:
				# We have to accommodate after last booking
				roomsAvailabilityByStartTime[possibleStartTime] = room

		sortedRoomBookingsByStart = sorted(roomsAvailabilityByStartTime.items())
		# Return just room with the soonest available date
		return sortedRoomBookingsByStart[0] 

	def _addBooking(self, bookingId, roomId, bookerName, startTime, endTime):
		# Create client if not in database
		if bookerName not in self.clientsByName:
			client = Person(bookerName)
			self.clientsByName[bookerName] = client
		else:
			client = self.clientsByName[bookerName]
			
		# Create room if not in database
		if roomId not in self.rooms:
			room = Room(roomId)
			self.rooms[roomId] = room
		else:
			room = self.rooms[roomId]

		booking = Booking(bookingId, client, room, startTime, endTime)
		self.bookings.append(booking)
		room.bookings[startTime] = booking


def main(argv):
	inputFile = 'data/smallSet.csv'
	durationInSeconds = 3600*3

	try:
		opts, args = getopt.getopt(argv,"hi:d:t",["ifile="])
	except getopt.GetoptError:
		help()
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			help()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputFile = arg
		elif opt in ("-d"):
			try:
				durationInSeconds = int(arg)
			except:
				help()
				sys.exit(2)
		elif opt in ("-t"):
			test()
			sys.exit()

	hotel = Hotel()
	hotel.loadFromFile(inputFile)
	(nextDate, room) = hotel.findNextAvailableBookingSlot(timedelta(seconds=durationInSeconds))
	print "Next available slot is " + str(nextDate) + " in room " + str(room.roomId)


def help():
	print """
Try booking.py -i <inputFile[=data/smallSet.csv]> -d <durationInSeconds[=10800]>

Parameters:
	-i = input file name (default is 'data/smallSet.csv')
	-d = duration in seconds (default is 3 hours so 10800)
	-h = this help
	-t = test run (will use data/smallSet.csv file and check next available booking slot function)
"""


def test():
	hotel = Hotel()
	hotel.loadFromFile('data/smallSet.csv')

	hotel.printBookings()
	hotel.printClients()
	hotel.printRooms()

	(nextDate, room) = hotel.findNextAvailableBookingSlot(timedelta(hours=5))
	print "Finding next Availble date for 5 hours " + str(str(nextDate) == "2015-04-02 00:23:05" and room.roomId == 7)
	(nextDate, room) = hotel.findNextAvailableBookingSlot(timedelta(hours=3))
	print "Finding next Availble date for 3 hours " + str(str(nextDate) == "2015-04-01 01:27:00" and room.roomId == 242)


if __name__ == "__main__":
   main(sys.argv[1:])