import os

def evaluateSize(byteSize):
	power = 2**10
	n = 0
	power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
	while byteSize > power:
		byteSize /= power
		n += 1
	return str(round(byteSize, 2)) + ' ' + power_labels[n]

def filesindir(folderpath=None, preferredTypeFilter=None, outputFileSizes=False):

	if folderpath!=None:
		
		folderpath = folderpath.rstrip("\\")+"\\"
		
		if preferredTypeFilter:
			files = [f for f in os.listdir(folderpath) if f.endswith(preferredTypeFilter)]
		else:
			files = os.listdir(folderpath)
		
		if not outputFileSizes:
			for i, f in enumerate(files):
				print(str(i) + " - " + f)
		else:
			for i, f in enumerate(files):
				print(str(i) + " - " + f + " (" + evaluateSize(os.path.getsize(folderpath+f)) + ")")
		
		a = int(input("number: "))
		return folderpath+files[a]
	else:
		print("Provide a file path")