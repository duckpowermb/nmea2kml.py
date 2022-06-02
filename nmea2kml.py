# -*- coding: utf-8 -*-
"""
NMEA to KML Convertor
@author: JingHui WU
@date: 06/02/2022

fork and modify from
https://github.com/msacwendychan/NMEAtoKML
"""

import os
import string
import sys
from tkinter.messagebox import NO
# Use nmeagram.py
import nmeagram
import re

# KML file template
KML_TEMPLATE = \
    """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name> NMEA to KML: %s</name>
  <Placemark>
      <name>Start Point</name>
          <Point>
              <coordinates>%s</coordinates>
              <altitudeMode>relativeToGround</altitudeMode>
          </Point>
  </Placemark>
 <Placemark>
      <name>End Point</name>
          <Point>
              <coordinates>%s</coordinates>
              <altitudeMode>relativeToGround</altitudeMode>
          </Point>
  </Placemark>
  <Placemark>
      <name> %s </name>
          <Style>
              <LineStyle>
                  <color>0xFF00FF00</color>
              </LineStyle>
		    </Style>
              <MultiGeometry>
                  <LineString>
                      <coordinates>%s</coordinates>
                      <altitudeMode>relativeToGround</altitudeMode>
                      <tessellate>1</tessellate>
                  </LineString>
              </MultiGeometry>
  </Placemark>
</Document>
</kml>"""

KML_EXT = ".kml"

start_point = None
end_point = None


def read_next_point_location(datafile):
    ret_str = None
    point = []
    point_is_ok = False

    while not point_is_ok:
        line = datafile.readline()
        if not line:
            break
        line2 = re.sub(r'\d\d-\d\d \d\d:\d\d:\d\d.\d\d\d ', '', line)
        if line2 != line:
            print("Remove TS %s ==> %s" % (line, line2))
            line = line2
        nmeagram.parseLine(line)
        if 0 == nmeagram.getField("Longitude"):
            continue
        point.append(str(nmeagram.getField("Longitude")))
        point.append(",")
        point.append(str(nmeagram.getField("Latitude")))
        ret_str = ''.join(point)
        point_is_ok = True
        print('hd line %s ret_str:%s' % (line, ret_str))

        global start_point, end_point
        if start_point is None:
            start_point = ret_str
        end_point = ret_str

    return ret_str


def getCoordlist(datafile):

    coordDataStr = ''
    line_parse = read_next_point_location(datafile)
    cor_num = 0
    # Reads a NMEA file by lines and returns lat and long coordinates
    while line_parse is not None:
        coordDataStr += line_parse + ' '
        line_parse = read_next_point_location(datafile)
        cor_num += 1
    print('Point Count:%d' % (cor_num))
    return coordDataStr

def main():
    datafile = None
    if len(sys.argv) == 2:
        print("Handling NMEA File:%s" % sys.argv[1])
        datafile = open(sys.argv[1], "r")
        fn = ".\\" + sys.argv[1] + KML_EXT
        fo = open(fn, 'w')
        point_list = getCoordlist(datafile)
        fo.write(KML_TEMPLATE %
                 (fn, start_point, end_point, fn, point_list))
        fo.close()
    else:
        print('this.py nema.log')

if __name__ == "__main__":
    main()
