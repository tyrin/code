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
import argparse
############################# parse input arguments #############################


argParser = argparse.ArgumentParser()
argParser.add_argument("-a", "--apexFile", help="Apex file name without extension")
argParser.add_argument("-t", "--type", help="Type or Method")
args = argParser.parse_args()
#print("args=%s" % args)
#apex_ConnectAPI_CdpDataEnrichment_getSourceObjects
#print("args.type=%s" % args.type) 
#print("args.apexFile=%s" % args.apexFile) 
apexPath = "./input/%s" % args.apexFile
#print(apexPath)
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

for child in root:
    print(child.tag, child.attrib)
    
print(root[3][3].text)
print(root.findall("./refbody/section[4]"))
#root.findall(".//section/..[@name='Singapore']")