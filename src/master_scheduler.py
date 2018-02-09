#!/usr/bin/python
import sys
import os

def main(argv):
	#validate input args
	index_len = len(sys.argv)
	if (index_len < 4):
		print "No input args, Need ip files and op location info\n"
		sys.exit(1)
	else:
		dataFile = argv[1]
		percentFile = argv[2]
		opFile = argv[3]

	if (dataFile == "" or percentFile == ""):
		print "Empty input file info\n"
		sys.exit(1)
	elif (opFile == ""):
		print "op file information missing\n"
		sys.exit(1)

	if (index_len > 4):
		print "Unwanted additional input info warning, execution contd...\n"

	#open input file and read contents
	if not os.path.exists(dataFile):
		print "Error," + " " + dataFile + "  doesnt exist\n"
		sys.exit(1)

	ipFile = open(dataFile,"r")
	for line in ipFile:
		fields = line.split('|')
		if (
			fields[15] == "" and fields[0] != "" and
			fields[7] != "" and fields[10] != "" and
			fields[13] != "" and fields[14] != ""
		   ):
			print fields[0]	#recipient id
			print fields[7] #name of donor
			print fields[10][:5] #zipcode of donor
			print fields[13] #date of donation
			print fields[14] #donation amount
			print "\n"
	ipFile.close()
	sys.exit(0)

if __name__ == "__main__":
	main(sys.argv)
