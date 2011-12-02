#!/usr/bin/python
# -*- coding: utf-8 -*-

#Author Diogo Bernardino
#Credits: simpleKML Project http://code.google.com/p/simplekml/

import json
import codecs
from xml.etree import ElementTree as ET
from simplekml import Kml #imports should be specific to avoid polluting or replacing previously loaded names


import argparse


class KMLParser:
	OUTPUT_FORMATS = ['terminal','txt','json','kml','kmz']

	RESULT_FILENAME = 'kmlinfo'

	def __init__(self, filename):
		tree = ET.parse(filename)
		#Obtain xmlns
		elem = tree.getroot()
		ns = elem.tag[:-3]

		#Internal geographical representation
		self.content = []

		for p in tree.iter(ns + 'Placemark'):
			for pelem in p:
				if pelem.tag == ns+'name':
					name = pelem.text
				elif pelem.tag == ns+'Point':
					coord = pelem.find(ns+'coordinates').text.split(',')
			self.content.append( (name, coord[0], coord[1]) )#stores a list of 3-element tuples

	def convert(self, output):
		output_filename = '{}.{}'.format(KMLParser.RESULT_FILENAME, output)
		if output in ['kml', 'kmz']: #check if value is in a list
			kmlinstance = Kml()
			folder = kmlinstance.newfolder()
			folder.name = "My Places"
			for name, lat, lon in self.content:#tuples can be decomposed in a for loop. This is the same as "for (x,y,z) in self.content" or "for t in self.content" and then using t[0] etc.
				folder.newpoint(name=name, coords=[(lat,lon)])
			kmlinstance.save( output_filename )
		elif output in ['terminal', 'txt']:
			newcontent = [ '%s\t->\t%.4f %.4f'%(name, float(lat),float(lon)) for name, lat, lon in self.content ] #list comprehensions rock!!
			if output == 'txt':
				f = open(output_filename, 'w')
				f.write( '\n'.join(newcontent) )
				f.close()
			elif output is 'terminal':
				print '\n'.join(newcontent)
		elif output == 'json':
			newcontent = [ {'name': name, 'coordinates': {'latitude':lat, 'longitude':lon} } for name, lat, lon in self.content ]
			f = open(output_filename, 'w')
			json.dump(newcontent, f, indent=2)
			f.close()


if __name__ == '__main__':
	#argparsemodule takes care of argument parsing and is easy to modify in the future
	arguments = argparse.ArgumentParser(description='Extract name and coordinates of points of a KML file')

	arguments.add_argument( '-f','--file', metavar='<Filename>', required=True, help='KML File containing coordinates.' )
	arguments.add_argument('-o','--output', default='terminal', choices=KMLParser.OUTPUT_FORMATS, help='Format of the output file.')

	options = arguments.parse_args()

	KMLParser(options.file).convert(options.output)
