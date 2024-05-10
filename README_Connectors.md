*CONNECTOR Generation utility*
These instructions assume you're working on a mac.
To generate files for the Connector Framework:

## CLONE

1) Clone the team repo into your home directory. If you're successful, the path to it is:
   /Users/(yourname)/data-connectors-plugins. 
   Click the arrow on the green Code button. Click the double box icon to copy the URL to the repo.
   The repo is available from https://git.soma.salesforce.com/a360/data-connectors-plugins
   Click the arrow on the green Code button and select the SSH tab. Click the double box icon to copy the URL to the repo.
2) Clone the code utilities repo into your home directory. If you're successful, the path to it is:
   /Users/(yourname)/code

## INSTALL

1) Install python:
	python3 (you can download and install this from https://www.python.org/downloads/)
	In terminal in home directory:
	pip install certifi
	if you already have certify installed, use: pip install --upgrade certifi
	
2) Add python to your path. (Not: mac os has a really old version of python installed by default, but using this will cause problems)
	a) In your home directory, create a text file called .bash_login
		In terminal type:  
		nano .bash_login
		This command will open the .bash_login document (or create it if it doesn’t already exist) in the easiest to use text editor in Terminal – Nano.
	b)Add the following to that file 
		export PATH="/path/to/python:$PATH"
	c)	In terminal type:  
		nano .bash_profile 
		Add this to the file:
		source ~/.bash_login
	d) to test this

	
3) Install pandas
	In terminal:
	pip3 install pandas
	
2) You need the following files and folders:
   templates (put the template for the file you want to generate in this folder)
   |
   output (look for output in this folder)
   |
   config (if you just want to generate a couple of new files, not everything in a folder)
   |
   connect.sh - top level script for default values
   connectorgen.py - script to run with different arguments

## RUN
1) To run with defaults:
	bash connect.sh
	
	To run with custom arguments
	 python3 connectorgen.py (arguments)
	
     -t", "--templateFile" use to specify template file in templates directory",	default=c360_a_connector_.xml
     -c", "--configDir" use to specify directory for config files",	default="data-connectors-cdata-jdbc: 
     -cc", "--customConfig" use to specify directory for config files",	default="config": specifies config directory by default  
     -tp", "--type" use to specify custom or standard directory for json files. The default="standard" -
               If you want to use the config directory, specify `custom`.
               
Syntax:
	Usage: specify the template
		python3 connectorgen.py -t templatefile 
	Examples:
		python3 connectorgen.py  -t c360_a_set_up_connection_.xml
		python3 connectorgen.py  -t c360_a_connector_.xml
	
	Usage: change the json file directory in the repo:
    		python3 connectorgen.py -t templatefile -tp custom -c configdir 
	Example:
    	python3 connectorgen.py  -t c360_a_create_data_stream_.xml -c data-connectors-athena-jdbc

	Usage: only transform the json files in the config directory in this repo
    		python3 connectorgen.py -t templatefile -tp custom 
	Example:
    	python3 connectorgen.py  -t c360_a_create_data_stream_.xml -tp custom 

   Usage: only transform the json files in a custom config directory with a custom template and a custom json directory
   		python3 connectorgen.py -t templatefile -tp custom -c data-connectors-athena-jdbc -cc ../../mycustomdir
   Example: 
    python3 connectorgen.py -t templatefile -tp custom -cc ../../mycustomdir
    
**What the script does**
The script replaces the variables in a template with the top level variables. It also generates simple steps based on the ConnectorAttributes.     
