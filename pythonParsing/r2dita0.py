# to run python3 r2dita.py
import yaml
from yaml import SafeLoader
from yaml import BaseLoader
import xmltodict
import numpy as np
import pandas as pd
from pandas import json_normalize
import os
import sys
from pprint import pprint
# lets say the yaml file is test_sample.yml
from pandas import json_normalize
from os import getcwd, path
from yaml import SafeLoader, load

#path_to_yaml = path.join(getcwd(), ..., "cdp_somple.raml")
#with open(path_to_yaml) as yaml_file:
#    yaml_contents = load(path_to_file, Loader=SafeLoader)
#yaml_df = json_normalize(yaml_contents)

with open('normalized.txt', 'w') as yaml_file:
    yaml_contents = load('cdp_sample.raml', Loader=SafeLoader)
yaml_df = json_normalize(yaml_contents)
print(yaml_df)