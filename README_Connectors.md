*CONNECTOR Generation utility*
To generate files for the Connector Framework:
1) Install:
	python3 (you can download and install this from https://www.python.org/downloads/)
	pip3 install requirements.txt
2) You need the following files and folders:
   templates (put the template for the file you want to generate in this folder)
   |
   output (look for output in this folder)
   |
   config (if you just want to generate a couple of new files, not everything in a folder)
   |
   connectorgen.py - script to run with different arguments
   connect.sh - top level script for default values

3) To run with defaults:
	bash connect.sh
	
	To run with custom arguements
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