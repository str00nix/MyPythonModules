import os
import time

def printlist(li):
	for a in li:
		print(a)

def main():
	
	#such that duplicates are avoided
	#fill
	nplistfileobjlocation = r''
	nplistfileobj = open(nplistfileobjlocation, 'a+')
	nplistfileobj.seek(0)
	
	filenamesinlist = set(nplistfileobj.read().split('\n')) #will be unordered
	
	#example: r'C:\Users\<username>\AppData\Roaming\Notepad++\backup'
	#fill
	filelistdirectory = r''
	
	os.chdir(filelistdirectory)
	
	tempdir = set(os.listdir())
	tempdir = tempdir - filenamesinlist
	
	FileNamesSortedByCreationOrModifiedDate = sorted(tempdir,
		key=lambda f:
			os.path.getctime(os.path.join(filelistdirectory, f))
			if
				time.ctime(os.path.getctime(os.path.join(filelistdirectory, f))) > time.ctime(os.path.getmtime(os.path.join(filelistdirectory, f)))
			else
				os.path.getmtime(os.path.join(filelistdirectory, f)))
	
	# printlist(FileNamesSortedByCreationOrModifiedDate)
	
	#fill
	dumpfileobjlocation = r''
	
	dumpfileobj = open(dumpfileobjlocation, 'ab')
	
	for f in FileNamesSortedByCreationOrModifiedDate:
		
		if not f.find("new ") == 0:
			print('skipping "' + f + '" (' + str(f.find("new ")) + ')')
			continue
		
		fullfilepath = os.path.join(filelistdirectory, f)
		
		currentfile = open(fullfilepath, 'rb')
		currentfilecontents = currentfile.read().decode("UTF-8")
		
		#name
		dumpfileobj.write('\n\n---{}---\n\n'.format(f).encode("UTF-8"))
		# dumpfileobj.write('\n//{}\n//{}\n\n\n'.format(str(time.ctime(os.path.getctime(f))) , str(time.ctime(os.path.getmtime(f)))).encode("UTF-8"))
		
		cretime = str(time.ctime(os.path.getctime(fullfilepath)))
		modtime = str(time.ctime(os.path.getmtime(fullfilepath)))
		
		#date(s) (if creation and modified date are the same, just write one of them)
		dumpfileobj.write('\n//{}\n\n\n'.format(cretime + '\n//' + modtime if cretime != modtime else modtime).encode("UTF-8"))
		
		#file content
		dumpfileobj.write(currentfilecontents.encode("UTF-8"))
		
		currentfile.close()
		
		nplistfileobj.write(f + "\n")
	
	
	dumpfileobj.close()
	nplistfileobj.close()

if __name__ == "__main__":
	main()