#!/usr/bin/python

# Simple gopher client test
import re
import sys
import socket

def dig(hole, cavern = ""):
	server = hole

	gophersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Connecting to server: ", server
	try:
		gophersock.connect((server, 70))
	except socket.gaierror, e:
		print "Error connecting to server: %s" % e
		return 0	
	fd = gophersock.makefile('rw', 0)
	fd.write(cavern +"\r\n")
	print(chr(27) + "[2J")

	linknum = 0
	#create our regular expression
	for line in fd.readlines():
		if line[0] == "i":
			line = line[1:]
		p = re.compile('.+(?=[\t][.a-zA-Z]+[\t][.a-zA-Z]+[\t][0-9]+)');
		pl = re.compile('.+(?=[\t][\/:\-_.a-zA-Z0-9]+[\t][.a-zA-Z0-9]+[\t][0-9]+)');
		pu = re.compile('[\t][\/:\-_.a-zA-Z0-9]+[\t][.a-zA-Z0-9]+[\t][0-9]+');
		thing = p.match(line)
		linkthing = pl.match(line);
		blankline = pu.match(line);
		if thing:
			if thing.group():
				print("\t\t"+thing.group())
			else:
				print("\n")
		elif linkthing:
			#otherthing = pf.match(line);
			if linkthing:
				whatisit = "";
				if (line[0] == "0"):
					whatisit = "TXT"
				elif(line[0] == "1"):
					whatisit = "DIR"
				elif(line[0] == "9"):
					whatisit = "FILE"
				else:
					whatisit = line[0] + "   "
				line = linkthing.group()
				line = line[1:]
				print linknum, " ", whatisit , "\t" , line
				linknum += 1
			else:
				print("\n")
		else:
			if blankline:
				print("\n")
			else:
				print "\t\t", line

while 1:
	print "\n\n"
	sendthegopher = raw_input(" > Enter Address and file or link number: ")
	if " " in sendthegopher:
		parts = sendthegopher.split(" ");
		dig(parts[0], parts[1])
	else:
		if sendthegopher[0] == "/":
			if sendthegopher[1:] == "quit":
				sys.exit(0)
			elif sendthegopher[1:] == "help":
				print "\nThis will be comming\n"
		else:
			try:
				int(sendthegopher)
				print "\nNot implemented yet sucker!\n"
			except ValueError:
				dig(sendthegopher)
