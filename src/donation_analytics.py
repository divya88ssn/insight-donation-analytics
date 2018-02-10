#!/usr/bin/python
import sys
import os
import math
from sortedcontainers import SortedList

def calcPercentile(percentile, ipList) :
	index = (int(percentile)/100) * len(ipList)
	value = (str(ipList[index]).split('.'))[1]
	if (int(value) >= 5) :
		retVal = math.ceil(ipList[index])
	else :
		retVal = math.floor(ipList[index])
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
	zipYrDict = {} #dictionary that uses zip+year as keys and\
			#SortedList() to store repeat contribution amount for a given zip+year

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

			#update total num of transactions for this rec+zip+year
			if not totalTransactions.has_key(recipientId) :
				totalTransactions.update({recipientId:1})
			else :
				sum = totalTransactions[recipientId] + 1
				totalTransactions[recipientId] = sum

			#for percentile calculation
			zipYrKey = fields[2]+fields[3][-4:]
			if not zipYrDict.has_key(zipYrKey) :
				amtList = SortedList()
				amtList.add(float(fields[4]))
				zipYrDict.update({zipYrKey:amtList})
			else :
				myList = zipYrDict[zipYrKey]
				myList.add(float(fields[4]))
				zipYrDict.update({zipYrKey:myList})
			value  = calcPercentile(percentile, zipYrDict[zipYrKey])

			opHandle.write(fields[0]+'|'+fields[2]+'|'+
					fields[3][-4:]+'|'+str(value)+'|'+str(long(totalAmount[recipientId]))+'|'+
					str(totalTransactions[recipientId])+"\n")
	opHandle.close()
	fileHandle.close()
	print "Success! script done executing, pls check "+ opFile + "\n"
	sys.exit(0)

if __name__ == "__main__" :
	main(sys.argv)
