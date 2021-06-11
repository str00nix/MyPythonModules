def getListFromLines(path = None):
	while not path:
		path = input("Specify a path:")
	txtfile = open(path,"r")
	return [w.rstrip("\n") for w in txtfile.readlines()]