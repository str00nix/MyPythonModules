import os
import time
from datetime import datetime

def main():
	
	#fill
	# outputlogpath = r""
	outputlogpath = input("directory for output file: ")
	if not os.path.exists(outputlogpath) or not os.path.isdir(outputlogpath):
		raise Exception("invalid input path")
	
	dirpath = ""
	
	while True:
		
		dirpath = input("directory to be logged (along with subdirs): ")
		
		if dirpath == "exit":
			break
		
		if not os.path.exists(dirpath) or not os.path.isdir(dirpath):
			# raise Exception("invalid input path")
			print("invalid input path")
			continue
		
		
		outputfilename = dirpath.replace(":","-").replace("\\","-")
		
		outputfile = open(os.path.join(outputlogpath, outputfilename) +"__"+str(datetime.now())[:-7].replace(" ","_").replace(":","-") + ".txt", "w", encoding = "utf-8")
		
		newlinechar = "\n"
		
		for path, subdirs, files in os.walk(dirpath):
			outputfile.write(f"\n---{path}---\n")
			cretime = str(time.ctime(os.path.getctime(path)))
			modtime = str(time.ctime(os.path.getmtime(path)))
			outputfile.write(f"{cretime + newlinechar + modtime if cretime != modtime else modtime}\n")
			
			for name in files:
				fullfilepath = os.path.join(path, name)
				
				cretime = str(time.ctime(os.path.getctime(fullfilepath)))
				modtime = str(time.ctime(os.path.getmtime(fullfilepath)))
				
				outputfile.write(f"\n{name}\n{cretime + newlinechar + modtime if cretime != modtime else modtime}\n{os.path.getsize(fullfilepath)}\n")
				
			outputfile.write("\n")
		
		outputfile.close()
		
	
	

if __name__ == '__main__':
	main()