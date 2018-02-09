#!/usr/bin/python
import sys
import os

def main(argv) :
	#validate input args
	index_len = len(sys.argv)
	if (index_len < 4) :
		print "donation_analytics.txt needs temp ip file, percentile value and op file name\n"
		sys.exit(1)
	else :
		processFile = argv[1]
		opFile = argv[2]
		percentile = argv[3]

	donorNameZip = {} #dictionary which uses donor name+zip as key
	totalAmount = {} #dictionary which uses recipient+zip+year as key
	totalTransactions = {} #dictionary that uses recipient+zip+year as key

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
				totalAmount.update({recipientId:long(fields[4])})
			else :
				sum = totalAmount[recipientId] + long(fields[4])
				totalAmount[recipientId] = sum

			#update total num of transactions for this rec+zip+year
			if not totalTransactions.has_key(recipientId) :
				totalTransactions.update({recipientId:1})
			else :
				sum = totalTransactions[recipientId] + 1
				totalTransactions[recipientId] = sum

			opHandle.write(fields[0]+'|'+fields[2]+'|'+
					fields[3][-4:]+'|'+""+'|'+str(totalAmount[recipientId])+'|'+
					str(totalTransactions[recipientId])+"\n")
	opHandle.close()
	fileHandle.close()
	sys.exit(0)

if __name__ == "__main__" :
	main(sys.argv)
