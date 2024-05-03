*CONNECT API utility*
These instructions assume you're working on a mac.

To generate the resources file for the Connect API:
1) Install:
	python3 (you can download and install this from https://www.python.org/downloads/)
	pip3 install requirements.txt
2) You need the following files and folders:
   input (put the spec in this folder)
   |
   output (look for output in this folder)
   |
   ca2dita.py
   processtext.pl

3) To run:
   python3 ca2dita.py -s (specFilename)
   Example
   `python3 ca2dita.py -s cdp-connect-api-RAML-59.0.raml`

**What the script does**
The script uses python to parse the RAML spec and traverse it recursively. 
Any values that aren't nested dictionaries are processed. 
Complex values, such as descriptions, use the processtext.pl script.
That's because perl lets you do multiple regex passes, which is needed to fix the formatting etc.

