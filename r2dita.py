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
import argparse
import json

############################# function to recursively process properties and dictionaries#############################
def process_text(findtext, replacetext, text):
	proctext = text.replace(findtext, replacetext)
	return str(proctext)
def process_dict(x, id, c): #where x is the spec dictionary, id is the base id, and c is the configdata
	for name, value in x.items():
		if isinstance(value, dict):
			newdict = x[str(name)]
			did1=str(name) #stringify the name for the dictionary id
			newdictid=re.sub(r'[^\w]', '', did1)
			newid = f'{id}_{newdictid}'
			process_dict(newdict, newid, c)
#	    elif isinstance(search_dict, list):
#        for element in search_dict:
#            item = get_recursively(element, field)
#            if item is not None:
#                return item
		else:
			for findstr, replacestr in c.items(): 
				#stringify value and escape special characters
				newtext = str(value)
				newtext = newtext.replace(findstr, replacestr) #This one and the next are functionally the same.
				#newtext = process_text(findstr, replacestr, newtext)
				#outputfile.write(f"New Text: {newtext}\n\n")
			#outputfile.write(f"Find string: {findstr}\n, Old Text: {value}\n, New Text: {newtext}\n\n")
			#print(f"      <p>{name}:<ph id=\"{id}_{name}\"> {newtext}</ph></p>\n")
			outputfile.write(f"      <p>{name}:<ph id=\"{id}_{name}\"> {newtext}</ph></p>\n")
############################# parse input arguments #############################
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--templateFile", help="template file in templates directory",  default="startresource.xml",)
argParser.add_argument("-s", "--specFile", help="spec file in input directory",  default="final.raml",)
args = argParser.parse_args()
#print("args=%s" % args)
#print("args.type=%s" % args.type) 
#print("args.specFile=%s" % args.specFile) 
specPath = "./input/%s" % args.specFile
print(f"specPath={specPath}")
templatePath = "./templates/%s" % args.templateFile
print(f"templatePath={templatePath}")

############################# load files and create output file #############################

#open RAML spec and read it in
inputfile = open("final.raml", "r")
data = inputfile.read()
inputfile.close()

#write out template
templatefile = open(templatePath, "r")
templatedata = templatefile.read()
templatefile.close()

#read in the text processing file
configfile = open("./templates/process.json", "r")
configdata = json.load(configfile) 
configfile.close()

#create the output file
outputfile = open("connectapi_resources.xml", "w")
outputfile.write(templatedata)

#Convert the yaml to a pdict
ramldict=yaml.safe_load(data)
#load the apex file and convert it to an etree
#tree = ET.parse(specPath)
#root = tree.getroot()

dictid = "capi"
process_dict(ramldict, dictid, configdata)
outputfile.write(f"\n    <section>\n")
outputfile.write(f"  </refbody>\n")
outputfile.write(f"</reference>")
outputfile.close()