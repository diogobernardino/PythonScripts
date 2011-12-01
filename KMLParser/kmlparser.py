#Autor Diogo Bernardino
#Credits: simpleKML Project http://code.google.com/p/simplekml/

import json
import codecs
import sys
from xml.etree import ElementTree as ET
from simplekml import *

resultfilename = 'kmlinfo'

args = sys.argv[1:]
if len(args) != 1:
    sys.exit('ERROR: Give me the filename argument!')
filename = args[0]

print 'Choose the output:\n 1 - Plain text file\n 2 - JSON file\n 3 - Simplified KML/KMZ file\n 4 - In terminal'
output = input('')

if output == 3:
	kmlinstance = Kml()
	folder = kmlinstance.newfolder()
	folder.name = "My Places"

tree = ET.parse(filename)

#parse xmlns
elem = tree.getroot()
ns = elem.tag[:-3]

#parse placemark elements and append to json content
content = ""
for p in tree.iter(ns + 'Placemark'):
	for pelem in p:
		if pelem.tag == ns+'name':
			name = pelem.text
		elif pelem.tag == ns+'Point':
			coord = pelem.find(ns+'coordinates').text.split(',',1)
	if output == 1 or output == 4:
		content = content + name + ' -> '+ ' '.join(coord) + '\n'
	elif output == 2:
		content = content +	json.dumps({'name': name, 'coordinates': {'latitude': coord[0], 'longitude':coord[1]}}) + ","	
	elif output == 3:
		folder.newpoint(name=name, coords=[(coord[0],coord[1])])
if output == 2:
	content = content[:-1] + "]"

#write file
if output == 1 or output == 2:
	if output == 1:
		f = codecs.open(resultfilename+".txt", 'w', "utf-8-sig")
	elif output == 2:
		f = codecs.open(resultfilename+".json", 'w', "utf-8-sig")
	f.write(content + "\n")
	f.close()
elif output == 3:
	format = input('KML or KMZ?\n 1 - KML\n 2 - KMZ\n')
	if format == 1:
		kmlinstance.save(resultfilename+".kml")
	else:
		kmlinstance.save(resultfilename+".kmz")
elif output == 4:
	print content
