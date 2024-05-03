This repo contains two utilities:

** [Connector documentation automation](./README_Connectors.md) **
This script generates documentation
There's a top line connect.sh bash script that runs three templates for the cdata connectors. 
However you can customize what you convert with the underlying connectorgen.py script arguments.

** [Connect API resource file generation](./README_ConnectAPI.md) **
This script generates a resource file with unique IDs that can be used 
to conref spec information into Apex classes. The IDs generated are based on the resource path, so 
they shouldn't change, even if the content changes, as long as the resource paths are the same.


