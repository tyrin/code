#!/usr/local/bin/perl
# Author: Tyrin Avery 8/23
# to run python3 conectorgen.py  
# to customize python3 connectorgen.py -t templatefile -c configdir -cc (configdir)
#example: python3 connectorgen.py  -t c360_a_set_up_connection_.xml
#example: python3 connectorgen.py  -t c360_a_create_data_stream_.xml
#example: python3 connectorgen.py  -t c360_a_connector_.xml
# -cc lets you process json files from the config directory

# example python3 test1.py -s cdp-connect-api-RAML-59.0.raml
import yaml
import xmltodict
import os
import glob
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
import configparser

############################# parse input arguments #############################
argParser = argparse.ArgumentParser()
argParser.add_argument("-t", "--templateFile", help="template file in templates directory",	default="c360_a_connector_.xml",)
argParser.add_argument("-c", "--configDir", help="directory for config files",	default="data-connectors-cdata-jdbc",)
argParser.add_argument("-cc", "--customConfig", help="directory for config files",	default="config",) #specifies config directory by default  
argParser.add_argument("-tp", "--type", help="custom or standard",	default="standard",) #if you want to use the config directory
args = argParser.parse_args()
#print("args=%s" % args)
#print("args.templateFile=%s" % args.templateFile) 
#print("args.configDir=%s" % args.configDir) 
#/Users/tavery/data-connectors-plugins/data-connectors-cdata-jdbc/src/main/resources/ConnectionDefinition

#if you just want to specify the connector group
if args.type == "standard": 
	configPath = "/Users/tavery/data-connectors-plugins/%s/src/main/resources/ConnectionDefinition" % args.configDir
	print(f"configPath={configPath}")
#if you just want to use a handful of custom configs, you can put them in the config directory
else:
	configPath = "./%s" % args.configDir
	print(f"customPath={customConfig}")

#print template path
templatePath = "./templates/%s" % args.templateFile


############################## create log file  #############################
#logfile = open("./output/connectorlog.txt", "w")

############################# get json files #############################
# to store files in a list
#list = []
 
# dirs=directories
#for (root, dirs, file) in os.walk(configPath):
#		for f in file:
#				if '.json' in f:
#						print(f)
						
for filename in glob.glob(os.path.join(configPath, '*.json')): # get a list of all the json files in the folder
	with open(os.path.join(os.getcwd(), filename), 'r') as f: # open each file in readonly mode
		#print(f)
		print(f"filename={filename}")
		configdata = json.load(f) 
		#print(type(configdata)) #tells me if it's a dict
		#print(configdata) #prints out the json string
		#for k, v in configdata.items(): #prints out the key value pairs
		#	print(k, v)
		print(configdata["label"])
		#print(configdata["connectionAttributes"])
		conattr = configdata["connectionAttributes"]
		#print(len(conattr)) #prints out how many attributes there are
		
		steps = "" #defining empty string to hold the step information
		for i in range(len(conattr)): #iterate through all the connection Attributes in the list
			#if conattr[i]["type"] == "custom":
			#	print(conattr[i]["dataType"])
			#	#if it's a combobox or checkbox do this
			if (conattr[i]["type"] == "custom") and (conattr[i]["dataType"] == "checkbox"):
					#print ("Check the box")
				boxname = conattr[i]["label"] 
				step = f"<substep><cmd>Check the {boxname} values to use.</cmd></substep>"
				steps += step
			elif (conattr[i]["type"] == "custom") and (conattr[i]["dataType"] == "combobox"):
					#print ("Check the box")
				comboname = conattr[i]["label"] 
				step = f"<substep><cmd>Select the {comboname} that you want to use.</cmd></substep>"
				steps += step
			#print(conattr[i]["name"])
			elif 'label' in conattr[i]:
				paramname = conattr[i]["label"]
				step = f"<substep><cmd>Enter a {paramname} value.</cmd></substep>"
				steps += step
			else:
				typename = conattr[i]["type"]
				step = f"<substep><cmd>Enter a {typename} value.</cmd></substep>"
				steps += step
		configdata["steps"] = steps #add the steps to the configdata dictionary
		#print(steps)
		#read in template
		print(f"templatePath={templatePath}")
		templatefile = open(templatePath, "r")
		templatedata = templatefile.read()
		templatefile.close()
		
		#print (templatedata)
		#replace the variables in the template with the values from the json file dictionary
		filedata = templatedata.format(**configdata) 
		#print (filedata)
		
		#create the output file
		#f = open('%s.csv' % outputfilename, 'wb')
		tempname = os.path.splitext(args.templateFile)[0]
		#print(tempname)
		outputfilename = tempname + configdata["name"] 
		outputfile = open(".//output//%s.xml" % outputfilename, "w")
		outputfile.write(filedata)


#logfile.close()

#add in test for article ie a vs an
#add in test for unresolved variables for file and throw error message to log
#get the root path for the repo to reference for the json files and update the args to allow you to pass in something else
#split the template name and use it for the output files.