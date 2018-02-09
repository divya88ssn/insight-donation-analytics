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

	#check if input files exist
	if not os.path.isfile(dataFile):
		print "Error, " + dataFile + "  doesnt exist\n"
		sys.exit(1)
	elif not os.path.isfile(percentFile):
		print "Error, " + percentFile + "  doesnt exist\n"
		sys.exit(1)

	#check if op file location is valid
	if not os.path.exists(opFile):
		print "Error, output file location doesnt exist \n"
		opFile = os.getcwd() + "/output/repeat_donors.txt"
		print "Taking default path as " + opFile + "\n"

	#create and write to an intermediate output file
	tempOpFile =  os.getcwd() + "/output/cleanedIpFile.txt"
	op = open(tempOpFile, "w+")

	#read from itcont.txt and select lines with valid fields
	ipFile = open(dataFile,"r")
	for line in ipFile:
		fields = line.split('|')
		if (
			fields[15] == "" and fields[0] != "" and
			fields[7] != "" and fields[10] != "" and
			fields[13] != "" and fields[14] != ""
		   ):
			op.write(fields[0]+"|"+fields[7]+"|"+fields[10][:5]+"|"+
					fields[13]+"|"+fields[14]+"\n")
	ipFile.close()
	op.close()

	#get percentile value from percentFile
	percentile = 10 #initialize percentile to some default
	percentFileHandle = open(percentFile, "r")
	for line in percentFileHandle:
		fields = line.split(' ')
		if (fields[0] != ""):
			percentile = fields[0]
		else:
			print "Empty percentile file\n"
			print "Default percentile value is taken to be " + percentile + "\n"
	percentFileHandle.close()

	#call the script that actually creates the repeat_donors.txt
	script = os.getcwd() +  "/src/donation_analytics.py"
	command = 'python ' + script + ' ' + tempOpFile + ' ' + opFile + ' ' + percentile
	if os.path.isfile(tempOpFile):
		os.system(command)
	else:
		print "No records of interest were found in input file\n"

	sys.exit(0)

if __name__ == "__main__":
	main(sys.argv)
