import os

def evaluateSize(byteSize):
	power = 2**10
	n = 0
	power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
	while byteSize > power:
		byteSize /= power
		n += 1
	return str(round(byteSize, 2)) + ' ' + power_labels[n]

def filesindir(folderpath=None, preferredTypeFilter=None, includeKeyWords=None, outputFileSizes=False):
	if folderpath:
	
		folderpath = folderpath.rstrip("\\")+"\\"
		
		files = os.listdir(folderpath)
		fullfoldersize = len(files)
		
		if preferredTypeFilter:
			files = [f for f in files if f.endswith(preferredTypeFilter)]
		
		if includeKeyWords:
			files = [f for f in files if all([ x in f for x in includeKeyWords ])]
		
		if not outputFileSizes:
			for i, f in enumerate(files):
				print(str(i) + " - " + f)
		else:
			for i, f in enumerate(files):
				print(str(i) + " - " + f + " (" + evaluateSize(os.path.getsize(folderpath+f)) + ")")
		
		if len(files) > 0:
			a = input("Number: ")
			while a < '0' or a > str(len(files)-1):
				a = input("Insert a valid number: ")
			return folderpath+files[int(a)]
		else:
			if fullfoldersize > len(files):
				raise Exception('All available files have been filtered out.')
			else:
				raise Exception('No files found in the given directory.')
		
	else:
		raise ValueError("Folder path not provided")