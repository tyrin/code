import json
#read in the text processing file
processfile = open("./templates/process.json", "r")
#processdata = processfile.read()
processdata = json.load(processfile) 
processfile.close()

#open RAML spec and read it in
inputfile = open("final.raml", "r")
data = inputfile.read()
inputfile.close()

#if isinstance(processdata, dict):
#	print("Yes, it's a dictionary")
#else:
#	vartype = type(processdata)
#	print("Oh no! It's a {vartype}." )
