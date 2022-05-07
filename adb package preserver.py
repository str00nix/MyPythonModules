import subprocess
import os
import shutil


#example: r"C:\Users\<usename>\AppData\Local\Android\Sdk\platform-tools\adb.exe"
#fill
adbpath = r""


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
			newname = packagelocation.strip("/").replace("/","--")
			
			result = subprocess.run([adbpath, "pull", packagelocation, initialdownloadpath], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
			print(result.stdout)
			
			#get first (and only) file in initialdownloadpath
			
			oldname = ''
			filenames = os.listdir(initialdownloadpath)
			
			if filenames:
				oldname = filenames[0]
				newname = newname if 'base.apk' in oldname else oldname
				shutil.move(os.path.join(initialdownloadpath, oldname), os.path.join(movingdownloadpath,newname))
			else:
				print('no "oldname" ({})'.format(packagelocation))
			
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
	
	
	#fill
	finaltransferfolder = r""
	while not os.path.exists(finaltransferfolder) or not os.path.isdir(finaltransferfolder):
		finaltransferfolder = input("Folder path where packages are transfered after pulling:")
	
	print()
	
	pullAllPackages(packagelocations, initialtransferfolder, finaltransferfolder)
	

if __name__ == "__main__":
	main()
	dummyinput = input("Press any key to continue...")