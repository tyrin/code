import os
import yaml
from yaml import SafeLoader
import xml.etree.ElementTree as et
import shutil
import xmltodict
from pprint import pprint
#from xml.dom import minidom



#So the basic idea here is to use yaml to load the yaml into a dict
# then to use xmltodict.unparse to convert it to xml
#then use ElementTree to make it into a DITA file, because you can control what the dita looks like
#
# Function to create a DITA file from a node
#

#open RAML spec and read it in
inputfile = open("final.raml", "r")
data = inputfile.read()
inputfile.close()

#Convert the yaml to a pdict
dict1=yaml.safe_load(data)
for keys in dic1.keys():
	
#Convert the pdict to xml - unfortunately it isn't valid xml
#xml_string=xmltodict.unparse(dict1, full_document=False)
xml_string=xmltodict.unparse(dict1['/'], full_document=False)
#print("The XML string is:")
#print(xml_string)

with open("test.xml", "w") as f:
	f.write(xml_string)

#xmlstr = minidom.parseString(et.tostring(xml_string)).toprettyxml(indent="   ")
#with open("New_Database.xml", "w") as f:
#	f.write(xmlstr)

##Insert it into a root to make it valid
#root = et.Element('root')
#txt = et.SubElement(root, xml_string)
#txt_string = et.dump(root)

#Construct a dita file
# set the DITA template files
template = "templates/template.dita"
# read in the template DITA file (a concept)
fp = open(template,"r")
tstring = fp.read()
fp.close()
# save doctype
p = tstring.find("<concept")
doctype = tstring[0:p]

def makeDITA(ts,ctp,node,idir):
	global node_data

	# maximum images per row
	maxrow = 3
	
	if debugMode():
		print("makeDITA",ctp,node.get("id"),node.text)
  
	
	# initialize the DITA XML
	root = fromstring(ts)
	tree = et.ElementTree()
	tree._setroot(root)
			
	node_text = node.text
	node_id = node.get("id")
	node_author = node.get("user")
	node_created = node.get("created")
	node_textp = node.get("path")
	
	# read in the node body text file
	fp = open(node_textp,"r")
	node_text = fp.read()
	fp.close()

	# set output id and file path
	ditaid = ctp+"_"+node_id
	ditafile = ditaid+".dita"

	if sorttype == SCHRON:
	 node_data[node_id] = [ctp,node_created,ditafile,"?"]
	else:
	 title_key = node.text.upper()
	 title_key = title_key.strip()
	 title_key = title_key.replace('\n','')
	 while '  ' in title_key:
		 title_key = title_key.replace('  ',' ')
	 node_data[node_id] = [ctp,title_key,node_created,ditafile,"?"]
	 
	title_date = titleDate(node_created)

	# get all the image elements for the node
	images = node.find("images")
	imagelist = iter(images)

	top_images = []
	bot_images = []
	
	# build the image lists
	for image in imagelist:
		top_images.append(image)
	   
	# common for all content types
	root.set("id",ditaid)
	titlee = root.find("title")
	# title
	if develMode():
	  title_date=title_date+" "+ditafile
	if longtitle:
	  titlee.text = node.text+" - "+title_date+", by "+node_author
	else:
		titlee.text = node.text

	# find the body
	conbody = root.find("conbody")

	# tags
	keywords = root.find("prolog/metadata/keywords")
	tags = node.find("tags")
	tlist = iter(tags)
	for t in tlist:
		indt = SubElement(keywords,"indexterm")
		indt.text = t.text

	# create a section for the top images
	if len(top_images)>0:
		section = SubElement(conbody,"section")
		section.set("id","images_top")
		sectp = SubElement(section,"p")
		ni = 0
		for imge in top_images:
		  imagefn = idir+'/'+imge.get("filename")
		  imagefn = imagefn.replace("\\","/")
		  img = SubElement(sectp,"image")
		  img.set("href",imagePath(imagefn))
		  if not imge.text==None:
			img.set("alt",imge.text)
		  ni=ni+1
		  if ni>=maxrow:
			  sectp = SubElement(section,"p")
			  ni=0
			  
		
	# create a section for the text
	
	# get filtered node text
	filtered = filterText(node_text)
		
	# write out text in case we bomb out trying to parse it
	fpp = open("debug.xml","w")
	fpp.write(filtered)
	fpp.close()
		
		
	# make sure text is valid XML
	try:
		section = XML(filtered)
		# make the root be a section
		section.tag = "section"
		section.set("id","node_text")
		if debugMode():
			print("filtered section:")
			print(tostring(section))
				
			
	except:
		webErrorLog("Invalid node text in:",ctp,node.get("id"),node.text)
		logText("Invalid node text")
		logText(" node id: "+node.get("id"))
		logText(" node_text:")
		logText(node_text)
		logText(" filtered text:")
		logText(filtered)
		logText(" ")
			
		section = SubElement(conbody,"section")
		sectp = SubElement(section,"p")
		sectp.text = "** invalid XML **"

	dita_sections = html2dita(section,ditafile,ditaid)
			
	# add the text as sections
	for dita_section in dita_sections:
		if debugMode():
		  print("dita_section:",tostring(dita_section))
		conbody.append(dita_section)
				 
	# create a section for the bottom images
	if len(bot_images)>0:
		section = SubElement(conbody,"section")
		section.set("id","images_bottom")
		sectp = SubElement(section,"p")
		ni=0
		for imge in bot_images:
		  imagefn = idir+'/'+imge.get("filename")
		  imagefn = imagefn.replace("\\","/")
		  img = SubElement(sectp,"image")
		  img.set("href",imagePath(imagefn))
		  if not imge.text==None:
			 img.set("alt",imge.text)
		  ni=ni+1
		  if ni>=maxrow:
			  sectp = SubElement(section,"p")
			  ni=0

	# patch things up for image href values
	imgs = root.findall("*//image")
	for img in imgs:
		ipath = img.get("href")
		ipath_base = os.path.basename(ipath)
		ipath_dir  = os.path.dirname(ipath)
		ipath_full = imagedir+"/"+ipath_base
		
		apath_full = actualPath(ipath_full)
		apath_base = os.path.basename(apath_full)
		
		if not os.path.exists(ipath_full):
			webErrorLog(ditafile)
			webErrorLog("missing image",ipath_full)
			img.set("href",os.path.dirname(ipath)+"/"+os.path.basename(missing_image))
		else:
			img.set("href",os.path.dirname(ipath)+"/"+apath_base)
		
	try:
		# return the DITA topic as a string
		retstr = tostring(root)
	except:
		webErrorLog("Oh oh!, the DITA file is not XML")
		dump(root)
		exit(0)
		
	return retstr




## create the node DITA topic
#makedita = makeDITA(tstring,ctp,node,imagedir_rel)
## append the doctype to the XML for the node
#dita_file = doctype+makedita.decode()
#outpath = ctypeout+os.sep+node_data[nid][NFNFT]
#outpathr = ctp+os.sep+node_data[nid][NFNFT]
#node_data[nid][NFPATH] = outpathr
#
## write the DITA source file out
#print("  writing",outpath)
#fp = open(outpath,"w")
#fp.write(dita_file)
#fp.close()
#								
#	print()