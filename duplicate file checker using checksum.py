import os
import hashlib
from collections import Counter


def main():
	
	rootpath = ''
	
	rootpath = input("path: ").rstrip('"').strip('"')
	
	if rootpath == "exit":
		return
		
	while not os.path.exists(rootpath) or not os.path.isdir(rootpath):
		print("invalid input file path ({})".format(rootpath))
		rootpath = input("path: ").rstrip('"').strip('"')
		if rootpath == "exit":
			return
	
	
	arr = []
	
	for path, subdirs, files in os.walk(rootpath):
	
		for name in files:
			
			filepath = os.path.join(path, name)
			
			binaryFileContent = open(filepath, 'rb').read()
			
			arr.append({
				"filepath":filepath,
				"sha256":hashlib.sha256(binaryFileContent).hexdigest(),
			})
			
			binaryFileContent = b''
	
	
	countedresult = Counter([a["sha256"] for a in arr])
	countedresult = {x: count for x, count in countedresult.items() if count > 1}
	countedresult = dict(sorted(countedresult.items(), key = lambda x: x[1], reverse = True))
	
	
	print("\n\n")
	
	for a in countedresult.keys():
		print("{} - {}".format(a, countedresult[a]))
		print("\n".join([z["filepath"] for z in arr if a == z["sha256"]]))
		print("\n\n")
	
	

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(getattr(e, 'message', repr(e)))
	
	dummmy = input('Press Enter to continue.')