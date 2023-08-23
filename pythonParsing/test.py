#!/usr/local/bin/perl
import yaml
import xmltodict
import os
import sys
from pprint import pprint
from pandas import json_normalize
from os import getcwd, path
from yaml import SafeLoader, load
import xml.etree.ElementTree as ET
import re #regular expressions
import string

############################# get the required values from the raml doc and replace the values in the etree#############################
# recursively process every item in the dictionary
#if the value in the item is a dictionary, then construct and Id and make it into a new dictionary (and recursively process it)
#if it's a property, then process it and print it out   
def process_dict(x,id): #where x is the dictionary to pass in
	for name, value in x.items():
		if isinstance(value, dict):
			newdict = x[str(name)]
			did1=str(name) #stringify the name for the dictionary id
			newdictid=re.sub(r'[^\w]', '', did1)
			newid = f'{id}_{newdictid}'
			process_dict(newdict, newid)
#	    elif isinstance(search_dict, list):
#        for element in search_dict:
#            item = get_recursively(element, field)
#            if item is not None:
#                return item
		else:
			outputfile.write(f"<p>{name}:<ph id=\"{id}_{name}\"> {value}</ph></p>")
def process_text(y)

############################# load the raml doc and parse it #############################


#open RAML spec and read it in
inputfile = open("final.raml", "r")
data = inputfile.read()
inputfile.close()
#Convert the yaml to a pdict
ramldict=yaml.safe_load(data)
#read in template files
templatefile = open("./templates/startresource.xml", "r")
templatedata = templatefile.read()
templatefile.close()
#read in the text processing file
processfile = open("./templates/process.json", "r")
processdata = processfile.read()
processfile.close()
#open output file
outputfile = open("connectapi_resources.xml", "w+")
outputfile.write(templatedata)
dictid = "capi"
process_dict(ramldict, dictid)

############################# write to file #############################

outputfile.write(f"\n    <section>\n")
outputfile.write(f"  </refbody>\n")
outputfile.write(f"</reference>")
outputfile.close()