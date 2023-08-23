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

apexPath = "template.dita"
############################# load the raml doc and parse it #############################

#open RAML spec and read it in
inputfile = open("final.raml", "r")
data = inputfile.read()
inputfile.close()

#Convert the yaml to a pdict
ramldict=yaml.safe_load(data)
#load the apex file and convert it to an etree
tree = ET.parse(apexPath)
root = tree.getroot()
############################# get the required values from the raml doc and replace the values in the etree#############################
def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d
    
def process_method(dmethod,id):
	for name, prop in dmethod.items():
		if isinstance(prop, dict):
			print(f"Dictionary: {name}</p> ")
		else:
			print(f"{name}:<ph id=\"{id}_{name}\"> {prop}</ph>")

#		if type({prop}) is dict:
#			print(f"Dictionary: {name}</p> ")
#		else:
#			print(f"  <p id=\"{id}{name}\">{prop}</p> ")
#		if name == 'displayName':
#			print(f"  <p id=\"{id}{name}\">{prop}</p> ")
#		elif name == 'description':
#			print(f"  <p>{name}{prop}</p> ")
#		elif name == 'responses':
#			print(f"  <p>{name}{prop}</p> ")
#		else:
#			print(f"  <p>{name}{prop}</p> ")
#iterate through the spec and add xml

#dtypes = ramldict["types"]
#for name, types in dtypes.items():
#	repid=str(name)
#	print(f"<section><title>{name}</title></section>/n ") 
#	dtype = dtypes[str(name)] #get the nested dictionary using the key name
#	for name, type in dtype.items():
#		typestr=str(name)
#		typeid = f'{repid}{typestr}'
##		print(f"type id = {typeid}")
#		if name != 'properties':
#			print(f"<p>{name}</p> ")
#			print(f"<p id=\"{typeid}\">{type}</p> ")
#		else:
#			dprops = dtype["properties"]
#			for name, props in dprops.items():
#				print(f"  <p>{name}</p> ")
#				dprop = dprops[str(name)]
#				for name, prop in dprop.items():
#					print(f"  <p>{name}</p> ")
#					print(f"  <p>{prop}</p> ")
dresources = ramldict["/ssot"]
for name, resources in dresources.items():
	r1=str(name)
	resid=re.sub(r'[^\w]', '', r1)
	print(f"<section><title>{name}</title></section>/n ") 
	dresource = dresources[str(name)]
	if name == 'displayName':
		print(f"<p>{name}</p> ") 
	else:
		for name, resource in dresource.items():
			r2=str(name)
			#remove nonalphnumeric characters from the ID string
			resid2=re.sub(r'[^\w]', '_', r2)
			resourceid = f'{resid}{resid2}'
			#print(f"{name}")
			#if it's a method 
			if name == 'get' or name == 'patch' or  name == 'post' or name == 'delete':
				dmethod1 = dresource[str(name)]
				process_method(dmethod1, resourceid)
			else: #if it's a property or nested endpoint
				if name == 'displayName':
					print(f"  <p id={resourceid}>Display Name: {resource}</p> ")
				if name != 'displayName':
					print(f"  <p>{name}{resource}</p> ") #if it's a property not a nested method
#				else: # it's probably a nested portion of the end point 
					#dclass1 = dresource[str(name)]
					#for name, class1 in dclass1.items():
					#	print(f"  <p>{name}</p> ") 
				
			#print(f"resource id = {resourceid}")
#			if name == 'displayName':
#				print(f"<p>{name}</p> ")
#				print(f"<p id=\"{resourceid}\">{resource}</p> ")
#			else:
#				dget = dresource["displayName"]
#				for name, props in dprops.items():
#					print(f"  <p>{name}</p> ")
#					dprop = dprops[str(name)]
#					for name, prop in dprop.items():
#						print(f"  <p>{name}</p> ")
#						print(f"  <p>{prop}</p> ")