#!/usr/bin/env python
import sys, os
from os import *

directory = os.getcwd()


try:
    path = directory + '\dist'
    #adds directory to path so can be executed by command line#
    sys.path.insert(1,path)
    print "Added Paths"
    exit()
except Exception, e:
    print str(e)
    exit()