#!/usr/local/bin/perl
# Author: Tyrin Avery 8/23
# to run python3 ca2dita.py -s specfile -t templatefile
# example python3 ca2dita.py -s cdp-connect-api-RAML-59.0.raml
import yaml
import xmltodict
import os
import sys
from pprint import pprint
from pandas import json_normalize
from os import getcwd, path
from yaml import SafeLoader, load
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
			#logfile.write(f"  newdict= {newdict}\n name={name}")
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			if name == "uriParameters":
				#outputfile.write(f"<section><title>{name}</title>\n  <dl>\n    <dlentry>\n")
				outputfile.write(f"<p><b>{name}</b></p>\n  <dl id=\"{newid}\">\n")
				for pname, pvalue in value.items():
					outputfile.write(f"    <dlentry>\n      <dt><varname>{pname}</varname></dt>\n")
					for prop, propval in pvalue.items():
						typestr="type"
						descstr="description"
						reqstr="required"
						if prop == typestr:
							outputfile.write(f"      <dd>Type: {propval}</dd>\n")
						elif prop == descstr:
							outputfile.write(f"      <dd>{propval}</dd>\n")
						elif prop == reqstr:
							outputfile.write(f"      <dd>Required: {propval}</dd>\n")
						else:
							outputfile.write(f"      <dd>{prop}{propval}</dd>\n") #catchall in case there's something weird
					outputfile.write(f"    </dlentry>\n")
				outputfile.write(f"  </dl>\n")
				#outputfile.write(f"</section>\n")
			else:
				outputfile.write(f"<p><b>{name}</b></p>\n")
				#logfile.write(f"  newiddict= {newid}\n")
				process_dict(newdict, newid)
		elif isinstance(value, list): #process enums and any other lists
			safeid = process_id(name) #this removes any characters not allowed by dita IDs.
			newid = f'{id}_{safeid}'
			outputfile.write(f"  <ul id=\"{newid}\">\n")
			for element in value: #enums are a list, rather than text or a dict
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

dictid = "capi"
process_dict(ramldict, dictid)
#process_dict(ramldict, dictid, configdata)
outputfile.write(f"\n    </section>\n")
outputfile.write(f"  </refbody>\n")
outputfile.write(f"</reference>")
outputfile.close()
logfile.close()