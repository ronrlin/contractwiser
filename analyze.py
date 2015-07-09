#!/usr/bin/python
import csv
import shutil

data = []
with open('classify.csv', 'rt') as csvfile:
	filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in filereader:
		data.append(row)

# Go through data and move files into directory structure by agreement type
cnt = 0
for record in data:
	filetype = record[2]
	filename = record[1]
	#print(filetype + " " + filename)
	try: 
		if filetype == 'UNKNOWN': 
			print(" none ")
			# do nothing
		elif filetype == 'DECODE ERROR':
			print(" none ")
			# do nothing
		elif filetype == 'CREDIT AGREEMENT':
			shutil.move('./data/' + filename, './data/credit/' + filename)
		elif filetype == 'PURCHASE AGREEMENT':
			shutil.move('./data/' + filename, './data/purchase/' + filename)
		elif filetype == 'MERGER AGREEMENT':
			shutil.move('./data/' + filename, './data/merger/' + filename)
		elif filetype == 'CONVERTIBLE DEBT':
			shutil.move('./data/' + filename, './data/convertible/' + filename)
	except IOError:
		print('file already moved.... ignoring the error.')


# what about false positives

def readDict():
	with open('classify.csv') as f:
	    reader = csv.DictReader(f, delimiter = ',')
	    for row in reader:
	    	print(row.keys())
	    return reader


