#!/usr/local/bin/perl
# Author: Tyrin Avery 8/23
# to run python3 r2dita.py -s specfile -t templatefile
# defaults to python3 r2dita.py -s final.raml  -t startresource.xml
# example python3 ca2dita.py -s cdp-connect-api-RAML-59.0.raml
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
import subprocess
import shlex

############################# function to recursively process properties and dictionaries#############################
def process_id(name):
	id1=str(name) #stringify the name for the dictionary id
	id2=re.sub(r'[^\w]', '', id1)
	id3=re.sub(r'\(', '', id2)
	#id4=re.sub(r'[^\w]', '', id1)
	return str(id3) 
	
def process_text(findtext, replacetext, text):
	proctext = text.replace(findtext, replacetext)
	return str(proctext)
	
def process_dict(x, id): #where x is the spec dictionary, id is the base id, and c is the configdata
	for name, value in x.items():
		if isinstance(value, dict): #if the value is a dictionary, then process it one way.
			#create new id
			newdict = x[str(name)]
			#did1=str(name) #stringify the name for the dictionary id
			#newdictid=re.sub(r'[^\w]', '', did1)
			#newid = f'{id}_{newdictid}'
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			process_dict(newdict, newid)
#	    elif isinstance(search_dict, list):
#        for element in search_dict:
#            item = get_recursively(element, field)
#            if item is not None:
#                return item
		else: #if it's just a text value, then
			#create new id
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			oldtext = str(value)
			desc = "description"
			exp = "example"
			if safeid == desc: #if it's a description, process it and write it out differently
				newtext=subprocess.run(['perl','processtext.pl', newid, oldtext], capture_output=True, text=True)
				#print(newtext.stdout)
				text= newtext.stdout
				#outputfile.write(f"      <p>{name}:<ph id=\"{id}_{name}\"> {oldtext}</ph></p>\n")
			elif safeid == exp:
				outputfile.write(f"      <codeblock>{oldtext}</codeblock>\n")
			else:
				outputfile.write(f"      <p>{name}:<ph id=\"{id}_{name}\"> {oldtext}</ph></p>\n")
			#newtext=subprocess.Popen(['perl','processtext.pl', newid, oldtext],stdout=subprocess.PIPE)
			#print(newtext.stdout.read())
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
inputfile = open(specPath, "r")
data = inputfile.read()
inputfile.close()

#write out template
templatefile = open(templatePath, "r")
templatedata = templatefile.read()
templatefile.close()

##read in the text processing file
#configfile = open("./templates/process.json", "r")
#configdata = json.load(configfile) 
#configfile.close()

#create the output file
outputfile = open("./output/connectapi_resources.xml", "w")
outputfile.write(templatedata)

#Convert the yaml to a pdict
ramldict=yaml.safe_load(data)
#load the apex file and convert it to an etree
#tree = ET.parse(specPath)
#root = tree.getroot()

dictid = "capi"
process_dict(ramldict, dictid)
#process_dict(ramldict, dictid, configdata)
outputfile.write(f"\n    </section>\n")
outputfile.write(f"  </refbody>\n")
outputfile.write(f"</reference>")
outputfile.close()