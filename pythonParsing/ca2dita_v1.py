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
import re

############################# function to recursively process properties and dictionaries#############################
def process_id(name):
	id1=str(name) #stringify the name for the dictionary id
	id2=re.sub(r'[^\w]', '', id1)
	id3=re.sub(r'[()]', '', id2)	
	#logfile.write(f"  safeid= {id3}\n")
	return str(id3) 
	
def process_text(findtext, replacetext, text):
	proctext = text.replace(findtext, replacetext)
	return str(proctext)
	
def process_dict(x, id): #where x is the RAML spec dictionary, id is the base id, and c is the configdata
	for name, value in x.items():
		if isinstance(value, dict): #if the value is a dictionary, then process it one way.s
			#create new id
			newdict = x[str(name)]
			outputfile.write(f"<p><b>{name}</b></p>\n")
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			#logfile.write(f"  newiddict= {newid}\n")
			process_dict(newdict, newid)
		elif isinstance(value, list): #process enums and any other lists
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			outputfile.write(f"  <ul id=\"{newid}\">\n")
			for element in value:
				outputfile.write(f"  <li>{element}</li>\n")
			outputfile.write(f"  </ul>\n")
		else: #if it's just a text value, then
			#create new id
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			#logfile.write(f"  newidleaf= {newid}\n")
			oldtext = str(value)
			desc = "description"
			exp = "example"
			enum = "enum"
			if safeid == desc: #if it's a description, process it and write it out differently
				newtext=subprocess.run(['perl','processtext.pl', newid, oldtext], capture_output=True, text=True)
				#print(newtext.stdout)
				text= newtext.stdout
				#logfile.write(f"  {name}:{newtext}\n")
				outputfile.write(f"  <p id=\"{newid}_{name}\">{text}</p>\n")
			elif safeid == exp:
				outputfile.write(f"  <codeblock id=\"{newid}_codeblock\">{oldtext}  </codeblock>\n")
			#elif safeid == enum:
			#	newtext=subprocess.run(['perl','processenum.pl', newid, oldtext], capture_output=True, text=True)
			#	enumtext= newtext.stdout
			#	logfile.write(f"  {name}:{enumtext}\n")
			#	outputfile.write(f"  <p id=\"{newid}_{name}\">{enumtext}</p>\n")
			else:
				outputfile.write(f"      <p>{name}:<ph id=\"{newid}\"> {oldtext}</ph></p>\n")
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
#open a log file for troubleshooting
logfile = open("./output/log.txt", "w")
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
logfile.close()