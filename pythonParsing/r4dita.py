#to run: python3 r4dita.py
import yaml
from yaml import SafeLoader
import xmltodict
import os
import sys
import declxml as xml
from pprint import pprint

#open RAML spec and read it in
inputfile = open("final.raml", "r")
data = inputfile.read()
inputfile.close()

#Convert the yaml to a pdict
ramldict=yaml.safe_load(data)
	#doc = None
#print(ramldict['title'])
#print(ramldict.keys())
#print(ramldict.get("baseUri"))
#print(myfamily["/ssot"]["name"])

def get_inner_dict(d):
    for _, v in d.items():
        if isinstance(v, dict):
            return get_inner_dict(v) 
        else:
            return d

for xkey in ramldict["/ssot"]:
	print("<section><title>", xkey,"</title></section>")
	foo = data.get(xkey,{}).get(ykey,{})False)
	print(foo)
#for x, y in ramldict["/ssot"].items():
#  print(x, y)
#print(ramldict[keys])
#for node in ramldict:
#	#if node1["version"] == 58.0:
#	if node == 'title':
#		node1_processor = xml.dictionary('title', [
#			xml.string('.', attribute='id'),
#			])
#
#		#xml.serialize_to_string(processor, pdict, indent='    ')
#		print(xml.serialize_to_string(node1_processor, ramldict, indent='    '))
#		break
#
#open a file to write to
#with open('raml.xml', 'w') as f:
	#iterate through the pdict 
	#	print("-----------------------This is for the " + key + " Key-----------------------")

							
#outputfile.close()