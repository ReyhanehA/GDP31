#!/usr/bin/env python

##file here for py2exe

import re, sys, time, optparse
from cgi import escape
from traceback import format_exc
from Queue import Queue, Empty as QueueEmpty
from threading import Timer
import subprocess

__version__ = "v1.2.0"

USAGE = "%prog [options]"
VERSION = "%prog v" + __version__

AGENT = "%s / %s - Built By Jake Drew" % ("Ctrl-S", __version__)

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def parse_options():

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-b", "--branch",
            action="store", default="master", dest="branch",
            help="Branch name")

    parser.add_option("-r", "--remote",
            action="store", default="origin", dest="remote",
            help="Remote name")
    
    parser.add_option("-c", "--commit",
            action="store", default="null", dest='"commit"',
            help="Commit Message - surround with \"Commit Message\"")

    parser.add_option("-t", "--time",
            action="store", type="int", default=5, dest="time",
            help="How often to update the repo")
    parser.add_option("-a", "--auto",
            action="store_true", dest="auto",
            help="Whether to Run a loop")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        #raise SystemExit, 1

    return opts, args

def git(opts):
    if(opts.commit == 'null'):
        localtime = time.asctime( time.localtime(time.time()) )
        string = "Commited_@_"+str(time.strftime("%H:%M:%S"))
    else:
        string = str(opts.commit).replace(' ', '-')
    subprocess.call("git pull", shell=True)
    subprocess.call("git add --all", shell=True)
    subprocess.call("git commit -m '%s'" % string , shell=True) 
    subprocess.call("git push", shell=True)  
 


def main():
    print AGENT
    opts, args = parse_options()
    print "\n"
    if (opts.auto != None):
        rt = RepeatedTimer(int(opts.time), git, opts)   
    else:
       git(opts)
    
    
        

main()
