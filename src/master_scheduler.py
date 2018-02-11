#!/usr/bin/python
import sys
import os
import string
import re
from datetime import datetime


def validateDate(date) :
	if(len(date) != 8) :
		return False;
	year = date[-4:]
	day = date[2:4]
	month = date[0:2]
	now = datetime.now()
	if (not day.isdigit() or not month.isdigit() or
		not year.isdigit()) :
		return False;
	if not (int(day) > 0 and int(day) < 32) :
		return False;
	if not (int(month) > 0 and int(month) < 13) :
		return False;
	if not (int(year) > 0 and int(year) <= int(now.year)) :
		return False;
	return True;


def validateName(name) :
	if (len(name) > 200) :
		return False;
	if (any(c.isdigit() for c in name)) :
		return False;
	if not (re.search('[a-zA-Z]', name)) :
		return False;
	invalidChars = set(string.punctuation.replace(",","").
				replace(".","").replace("&","").
				replace("(","").replace(")","").
				replace("/","").replace("'","").
				replace("-",""))
	if (any(char in invalidChars for char in name)) :
		return False;
	return True;


def validateAmt(tranAmt) :
	number = tranAmt.split('.')[0]
	if (len(number) != len(tranAmt)) :
		decimal = tranAmt.split('.')[1]
		if (len(decimal) > 2) :
			return False;
		if (len(number+decimal) == 0 or len(number+decimal) > 14) :
			return False;
		if (not number.isdigit() or not decimal.isdigit()) :
			return False;
	else :
		if (len(tranAmt) > 14 or not tranAmt.isdigit()) :
			return False;
	return True;


def validateIpFields(cmteId, name, zipCode,
			tranDate, tranAmt) :
	#validate cmteId
	if (len(cmteId) != 9) :
		return False;
	#validate name
	isValid = validateName(name)
	if not isValid :
		return isValid;
	#validating zipCode
	if  (len(zipCode) < 5 or len(zipCode) > 9) :
		return False;
	elif not (zipCode.isdigit()) :
		return False;
	#validating date
	isValid = validateDate(tranDate)
	if not isValid :
		return isValid;
	#validate amount
	isValid = validateAmt(tranAmt)
	if not isValid :
		return isValid;
	return True;

def main(argv) :
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
		print "Warning, output file location doesnt exist \n"
		opFile = os.getcwd() + "/output/repeat_donors.txt"
		print "Continuing script execution taking default path as " + opFile + "\n"

	#create and write to an intermediate output file
	tempOpFile =  os.getcwd() + "/output/cleaned_ip.txt"
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
			isValid = validateIpFields(fields[0], fields[7], fields[10],
						fields[13], fields[14])
			if isValid :
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
	if (float(percentile) < 0 or float(percentile) > 100) :
		print "Invalid percentile value: Valid range is: 0 <=  percentile <= 100\n"
		sys.exit(1)

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
