#!/usr/bin/env python
import pika, time, sys, os
from datetime import date
def check():
	today = date.today()
	Max = date(2015,01,01)
	Min = date(2014,01,01)
	if Max <= today or today <= Min:
		print "Error."
		sys.exit()
		
extension = ".zip"
zippath = '.'
check()


UNC_PATH = raw_input("Please enter the UNC PATH: ")
UNC_PATH = os.path.normpath(UNC_PATH)
PASSWORD = raw_input("Please enter in globaly used PASSWORD(press enter if none):")

for (path, dirs, files) in os.walk(zippath):
	print "working.."
	filelist=[file for file in files if file.lower().endswith(extension)]

for file in filelist:
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(
					   'datacopym01.ctecfts.com'))
		channel = connection.channel()
		channel.queue_declare(queue='unzip_queue', durable=True)
		message = UNC_PATH+"\\"+file+":"+PASSWORD

		channel.basic_publish(exchange='',
				routing_key='unzip_queue',
				body=message,
				properties=pika.BasicProperties(
				delivery_mode = 2, # make message persistent
				))
		print " [x] Sent %r" % (message,)
		connection.close()
	except:
		print "There was a error somewhere"
