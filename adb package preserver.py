import subprocess
import os
import shutil


#example: r"C:\Users\<usename>\AppData\Local\Android\Sdk\platform-tools\adb.exe"
#fill if adb path is not specified
adbpath = r""

adbpathlist = [pathvarline for pathvarline in os.environ["path"].split(";") if 'adb.exe' in pathvarline or os.path.join("Android", "Sdk", "platform-tools") in pathvarline]

if not adbpath and (not len(adbpathlist) or not os.path.exists(adbpathlist[0])):
	raise Exception("invalid adb path")

if not adbpath:
	adbpath = adbpathlist[0]

print(adbpath)


def printlist(li):
	for line in li:
		print(line)

def getAllPackages():
	return [package.split("package:")[1] for package in str(subprocess.check_output('"{}" shell pm list packages'.format(adbpath), shell=True).decode()).splitlines() if package]


def getAllPackageLocations(listofallpackagenames):
	
	listofallpackagenames = [package.split("package:")[-1].rstrip() for package in listofallpackagenames if package]
	
	allpackagelocations = []
	
	for package in listofallpackagenames:
		packagelocation = str(subprocess.check_output('{} shell pm path {}'.format(adbpath, package), shell=True).decode())
		print("{} -> {}".format(package, packagelocation))
		allpackagelocations.append(packagelocation)
	
	return [packagelocation.split("package:")[-1].rstrip() for packagelocation in allpackagelocations if packagelocation]


def pullAllPackages(packagelocationlist, initialdownloadpath, movingdownloadpath):
	
	for packagelocation in packagelocationlist:
		
		try:
			result = subprocess.run([adbpath, "pull", packagelocation, initialdownloadpath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			
			print(result.stdout)
			
			oldname = packagelocation[packagelocation.rindex('/')+1:]
			
			if 'base.apk' in oldname:
				newname = packagelocation.strip("/").replace("/","--")
			else:
				newname = oldname
			
			shutil.move(os.path.join(initialdownloadpath, oldname), os.path.join(movingdownloadpath,newname))
			
		except Exception as e:
			print(getattr(e, 'message', repr(e)))
		
		print('\n---\n')

def main():
	
	packagelist = getAllPackages()
	printlist(packagelist)
	
	print('\n\n---\n\n')
	
	packagelocations = getAllPackageLocations(packagelist)
	# printlist(packagelocations)
	
	#fill
	initialtransferfolder = r""
	while not os.path.exists(initialtransferfolder) or not os.path.isdir(initialtransferfolder):
		initialtransferfolder = input("Folder path where packages are pulled:")
	
	
	finaltransferfolder = os.path.join(initialtransferfolder, "FinalDestination")
	if not os.path.isdir(finaltransferfolder):
		try:
			os.mkdir(finaltransferfolder)
		except OSError:
			if not os.path.isdir(finaltransferfolder):
				raise
	
	print()
	
	pullAllPackages(packagelocations, initialtransferfolder, finaltransferfolder)
	

if __name__ == "__main__":
	main()
	dummyinput = input("Press enter to continue...")