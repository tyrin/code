import yaml
from yaml import SafeLoader
#to run: python3 r3dita.py
from yaml import BaseLoader
from yaml import FullLoader
import xmltodict
import numpy as np
import pandas as pd
import os
import sys
from dict2xml import dict2xml
#open RAML spec and read it in
inputfile = open("./input/final.raml", "r")
data = inputfile.read()
inputfile.close()

#Convert the yaml to a pdict
fulldict=yaml.load(data,Loader=SafeLoader)
# Converting Python Dictionary to XML
#xml = dict2xml(data, wrap="all", indent="  ")
#wrap is the tag
xml = dict2xml.Converter(wrap="", indent=" ", newlines=True)
print(xml)
outputfile=open("connectResource.xml", 'w', encoding='utf-8')
with open('raml.xml', 'w') as f:
  f.write(str(xml))
outputfile.close()
