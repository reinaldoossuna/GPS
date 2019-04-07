# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.2
#   kernelspec:
#     display_name: Python [conda env:ic]
#     language: python
#     name: conda-env-ic-py
# ---

# +
from zipfile import ZipFile

filename = "DATA/RBMC_2017.kmz"

kmz = ZipFile(filename, 'r')
kml = kmz.open("doc.kml",'r')


# +
import xml.sax, xml.sax.handler

class PlacemarkHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.inName = False # handle XML parser events
        self.inPlacemark = False
        self.mapping = {} 
        self.buffer = ""
        self.name_tag = ""
        
    def startElement(self, name, attributes):
        if name == "Placemark": # on start Placemark tag
            self.inPlacemark = True
            self.buffer = "" 
        if self.inPlacemark:
            if name == "name": # on start title tag
                self.inName = True # save name text to follow
            
    def characters(self, data):
        if self.inPlacemark: # on text within tag
            self.buffer += data # save text if in title
            
    def endElement(self, name):
        self.buffer = self.buffer.strip('\n\t')
        
        if name == "Placemark":
            self.inPlacemark = False
            self.name_tag = "" #clear current name
        
        elif name == "name" and self.inPlacemark:
            self.inName = False # on end title tag            
            self.name_tag = self.buffer.strip()
            self.mapping[self.name_tag] = {}
        elif self.inPlacemark:
            if name in self.mapping[self.name_tag]:
                self.mapping[self.name_tag][name] += self.buffer
            else:
                self.mapping[self.name_tag][name] = self.buffer
        self.buffer = ""



# +
parser = xml.sax.make_parser()
handler = PlacemarkHandler()
parser.setContentHandler(handler)
parser.parse(kml)
kmz.close()


def build_table(mapping):
    sep = ','
        
    output = 'Name' + sep + 'lat' + sep + "long" + "\n"

    lines = ''

    for key in mapping:
        coord_str = mapping[key]['coordinates']
        coord_str = coord_str.strip().split(",")
        lat = coord_str[1]
        long = coord_str[0]
        lines += key + sep + lat + sep + long + "\n"
    output +=  lines
    return output



# -

outstr = build_table(handler.mapping)
out_filename = filename[:-3] + "csv" #output filename same as input plus .csv
f = open(out_filename, "w")
f.write(outstr)
f.close()
