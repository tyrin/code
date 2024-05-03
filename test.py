#!/usr/local/bin/perl
# Author: Tyrin Avery 5/24
#test class provided to test anything you like. It's not used by any script utility
# to run python3 test.py  

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
homepath = os.path.expanduser('~')
#print("homepath=%s" % homepath)
#if you just want to specify the connector group
if args.type == "standard": 
	configPath = f"{homepath}/data-connectors-plugins/{args.configDir}/src/main/resources/ConnectionDefinition"
	print(f"configPath={configPath}")
#if you just want to use a handful of custom configs, you can put them in the config directory
else:
	configPath = "./%s" % args.configDir
	print(f"customPath={customConfig}")