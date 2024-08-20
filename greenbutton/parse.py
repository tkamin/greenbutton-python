#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

import os, time
from datetime import timedelta

from resources import *

def parse_str(xml):
    tree = ET.ElementTree(ET.fromstring(xml))
    return extract_tree(tree)

def parse_feed(filename):
    tree = ET.parse(filename)
    return extract_tree(tree)

def extract_tree(tree):
    usagePoints = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:UsagePoint/../..', ns):
        up = UsagePoint(entry)
        usagePoints.append(up)
    
    meterReadings = []    
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:MeterReading/../..', ns):
        mr = MeterReading(entry, usagePoints=usagePoints)
        meterReadings.append(mr)

    for entry in tree.getroot().findall('atom:entry/atom:content/espi:LocalTimeParameters/../..', ns):
        ltp = LocalTimeParameters(entry, usagePoints=usagePoints)

    readingTypes = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:ReadingType/../..', ns):
        rt = ReadingType(entry, meterReadings=meterReadings)
        readingTypes.append(rt)

    intervalBlocks = []
    for entry in tree.getroot().findall('atom:entry/atom:content/espi:IntervalBlock/../..', ns):
        ib = IntervalBlock(entry, meterReadings=meterReadings)
        intervalBlocks.append(ib)
    
    return usagePoints

if __name__ == '__main__':
    os.environ['TZ'] = 'GMT'
    time.tzset()

    ups = parse_feed(sys.argv[1])
    for up in ups:
        print('UsagePoint (%s) %s %s:' % (up.title, up.serviceCategory.name, up.status))
        for mr in up.meterReadings:
            print('  Meter Reading (%s) %s:' % (mr.title, mr.readingType.uom.name))
            for ir in mr.intervalReadings:
                print('    %s, %s: %s %s' % (ir.timePeriod.start, ir.timePeriod.duration, ir.value, ir.value_symbol))
                #if ir.cost is not None:
                #    print(' (%s%s)' % (ir.cost_symbol, ir.cost))
                #if len(ir.readingQualities) > 0:
                #    print('[%s]' % ', '.join([rq.quality.name for rq in ir.readingQualities]))
                #print

    with open(sys.argv[1], 'r') as file:
        file_content = file.read()
        print(len(file_content))
        ups = parse_str(file_content)
        for up in ups:
            print('UsagePoint (%s) %s %s:' % (up.title, up.serviceCategory.name, up.status))
            for mr in up.meterReadings:
                print('  Meter Reading (%s) %s:' % (mr.title, mr.readingType.uom.name))
                for ir in mr.intervalReadings:
                    print('    %s, %s: %s %s' % (ir.timePeriod.start, ir.timePeriod.duration, ir.value, ir.value_symbol))
                    #if ir.cost is not None:
                    #    print(' (%s%s)' % (ir.cost_symbol, ir.cost))
                    #if len(ir.readingQualities) > 0:
                    #    print('[%s]' % ', '.join([rq.quality.name for rq in ir.readingQualities]))
                    #print
