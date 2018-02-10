#!/usr/bin/python
import sys
import os
import math
from sortedcontainers import SortedList


#routine to roundup a float to nearest float val
#
def roundUp(floatVal) :
	value = (str(floatVal).split('.'))[1]
	if (int(value) >= 5) :
		retVal = math.ceil(floatVal)
	else :
		retVal = math.floor(floatVal)
	return retVal;


#routine to return the running percentile of
#donations for a given zip and year
#
def calcPercentile(percentile, ipList) :
	index = (int(percentile)/100) * len(ipList)
	retVal = roundUp(ipList[index])
	return long(retVal);


def main(argv) :
	#validate input args
	index_len = len(sys.argv)
	if (index_len < 4) :
		print "donation_analytics.txt needs ip file, percentile and op file values\n"
		sys.exit(1)
	else :
		processFile = argv[1]
		opFile = argv[2]
		percentile = argv[3]

	donorNameZip = {} #dictionary which uses donor name+zip as key
	totalAmount = {} #dictionary which uses recipient+zip+year as key
	totalTransactions = {} #dictionary which uses recipient+zip+year as key
	recZipYrDict = {} #dictionary that uses recipient+zip+year as key and\
			#SortedList() to store every repeat contribution amount

	#create and write to the designated output file
	opHandle = open(opFile, "w+")

	fileHandle = open(processFile, "r")
	for line in fileHandle :
		fields = line.split('|')
		#check for repeat donor
		donorId = fields[1]+fields[2]
		if not donorNameZip.has_key(donorId) :
			donorNameZip.update({donorId:1})
		else :
			#update repeat donor info
			recipientId = fields[0]+fields[2]+fields[3][-4:]

			#update total amt received for this recipient+zip+year
			if not totalAmount.has_key(recipientId) :
				totalAmount.update({recipientId:float(fields[4])})
			else :
				sum = totalAmount[recipientId] + float(fields[4])
				totalAmount[recipientId] = sum
			totAmtForRecId = roundUp(totalAmount[recipientId])

			#update total num of transactions for this rec+zip+year
			if not totalTransactions.has_key(recipientId) :
				totalTransactions.update({recipientId:1})
			else :
				sum = totalTransactions[recipientId] + 1
				totalTransactions[recipientId] = sum

			#for percentile calculation
			if not recZipYrDict.has_key(recipientId) :
				amtList = SortedList()
				amtList.add(float(fields[4]))
				recZipYrDict.update({recipientId:amtList})
			else :
				myList = recZipYrDict[recipientId]
				myList.add(float(fields[4]))
				recZipYrDict.update({recipientId:myList})
			runningPer  = calcPercentile(percentile, recZipYrDict[recipientId])

			opHandle.write(fields[0]+'|'+fields[2]+'|'+
					fields[3][-4:]+'|'+str(runningPer)+'|'+
					str(long(totAmtForRecId))+'|'+
					str(totalTransactions[recipientId])+"\n")
	opHandle.close()
	fileHandle.close()
	print "Success! script done executing, pls check "+ opFile + "\n"
	sys.exit(0)

if __name__ == "__main__" :
	main(sys.argv)
