#!/usr/bin/python

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
					booking['bookingId'], 
					booking['roomId'],
					booking['bookerName'],
					Formatters.fromTimeWithTimezoneUTC(booking['startTime']),
					Formatters.fromTimeWithTimezoneUTC(booking['endTime']))


	def printBookings(self):
		print "Bookings:"
		for booking in self.bookings:
			print(str(booking.bookingId) + ", " + str(booking.startTime) + "-" + str(booking.endTime) + 
				" for " + booking.client.name + " in room " + booking.room.roomId)

	def printRooms(self):
		print "Rooms:"
		for room in self.rooms.itervalues():
			print room.roomId

	def printClients(self):
		print "Clients:"
		for clientName, client in self.clientsByName.iteritems():
			print str(client.personId) + ": " + client.name


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


def main():
	print "Hello world"

	hotel = Hotel()
	hotel.loadFromFile('data/smallSet.csv')
	hotel.printBookings()
	hotel.printClients()
	hotel.printRooms()

if __name__ =='__main__':main()