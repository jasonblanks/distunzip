#!/usr/bin/env python
import pika, time, os

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'datacopym01.ctecfts.com'))
channel = connection.channel()

channel.queue_declare(queue='unzip_queue', durable=True)
def callback(ch, method, properties, body):
	print " [x] Received %r" % (body,)
	MESSAGE = body.split(':')
	TEMP = os.path.split(MESSAGE[0])
	UNC_PATH = TEMP[0]
	UNC_PATH = os.path.normpath(UNC_PATH)
	print UNC_PATH
	FILE = TEMP[1]
	print FILE

	PASSWORD = os.path.split(MESSAGE[1])
	PASSWORD = PASSWORD[1]
	print PASSWORD
	#UNC_PATH = os.path.normpath(UNC_PATH)

	if not os.path.isdir(UNC_PATH+"\\extracts"):
		print UNC_PATH+"\\extracts"
		os.system("MD "+UNC_PATH+"\\extracts")
	
	if PASSWORD:
		#print "7z x -p\""+PASSWORD+"\" -o\""+UNC_PATH+"\\extracts\" \""+UNC_PATH+"\\"+FILE+"\"+r'>>"'+UNC_PATH+"\\extracts\\log.txt\""
		os.system("7z x -p\""+PASSWORD+"\" -o"+UNC_PATH+"\\extracts "+UNC_PATH+"\\"+FILE+">>"+UNC_PATH+"\\extracts\\"+FILE+".txt")
		print "7z x -p\""+PASSWORD+"\" -o"+UNC_PATH+"\\extracts "+UNC_PATH+"\\"+FILE+">>"+UNC_PATH+"\\extracts\\"+FILE+".txt"
		#os.system("7z x -p"+PASSWORD+" -o"+UNC_PATH+"\\extracts "+UNC_PATH+"\\"+FILE+r'>>'+UNC_PATH+"\\extracts\\log.txt")
	else:
		os.system("7z x -o"+UNC_PATH+"\\extracts "+UNC_PATH+"\\"+FILE+">>"+UNC_PATH+"\\extracts\\"+FILE+".txt")
		
	print " [x] Done"
	ch.basic_ack(delivery_tag = method.delivery_tag)
	
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,queue='unzip_queue')
					  
print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()


