import subprocess
import os
import shutil


#example: r"C:\Users\<usename>\AppData\Local\Android\Sdk\platform-tools\adb.exe"
#fill
adbpath = r""


def printlist(li):
	for a in li:
		print(a)

def getAllPackages():
	return [a.split("package:")[1] for a in str(subprocess.check_output('"{}" shell pm list packages'.format(adbpath), shell=True).decode()).split("\n") if a]


def getAllPackageLocations(listofallpackagenames):
	
	listofallpackagenames = [a.split("package:")[-1].rstrip() for a in listofallpackagenames if a]
	
	allpackagelocations = []
	
	for a in listofallpackagenames:
		allpackagelocations.append(str(subprocess.check_output(f'{adbpath} shell pm path {a}', shell=True).decode()))
	
	return [a.split("package:")[-1].rstrip() for a in allpackagelocations if a]


def pullAllPackages(packagelocationlist, initialdownloadpath, movingdownloadpath):
	
	for a in packagelocationlist:
		
		try:
			newname = a.strip("/").replace("/","--")
			
			result = subprocess.run([adbpath, "pull", a, initialdownloadpath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			print(result.stdout)
			
			#get first (and only) file in initialdownloadpath
			
			oldname = ''
			filenames = os.listdir(initialdownloadpath)
			
			if filenames:
				oldname = filenames[0]
				newname = newname if 'base.apk' in oldname else oldname
				shutil.move(os.path.join(initialdownloadpath, oldname), os.path.join(movingdownloadpath,newname))
			else:
				print('no "oldname" ({})'.format(a))
			
		except Exception as e:
			print(getattr(e, 'message', repr(e)))
		
		print('\n\n---\n\n')

def main():
	
	packagelist = getAllPackages()
	printlist(packagelist)
	
	print('\n\n---\n\n')
	
	packagelocations = getAllPackageLocations(packagelist)
	printlist(packagelocations)
	
	#fill
	initialfolder = r""
	transferfolder = r""
	pullAllPackages(packagelocations, initialfolder, transferfolder)
	

if __name__ == "__main__":
	main()
	dummyinput = input("Press any key to continue...")