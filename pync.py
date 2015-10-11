#!/usr/bin/env python
# Pync - Python Sync Utility
# Author: Jacob Gersztyn(@jabcog)

import os
import sys
import shutil
import filecmp
import argparse
from stat import *
import re
from fnmatch import translate

parser = argparse.ArgumentParser()
parser.add_argument("source", help="directory to sync from")
parser.add_argument("dest", help="directory to sync to")
parser.add_argument("-v", "--verbose", help="increase output verbosity", 
        action="store_true")
parser.add_argument("-q", "--quiet", help="""suppress output, except errors, 
        OVERRIDES --verbose""", action="store_true")
parser.add_argument("-n", "--no-action", help="""do NOT copy files, only print 
        what would happen""", action="store_true")
args = parser.parse_args()

realverbose = args.verbose and not args.quiet

def getIgnore(ignoreFile):
    home = os.path.expanduser("~")
    filepath = home+'/'+ignoreFile
    if realverbose:
        print(filepath)
    file = open(filepath, 'r')
    if realverbose:
        print('Using file ',file)
    patterns=[]
    for line in file:
        if line and line[0] != '#':
            if realverbose:
                print("This line is acceptable")
                print(line)
                print("Adding pattern: ",line.rstrip())
                print("Adding pattern: ",translate(line.rstrip()))
            patterns.append(translate(line.rstrip()))
    if realverbose:
        print("Patterns: ",patterns)

    return patterns


def sync(src,dest,verbose=False,quiet=False,no_action=False):
    patterns = getIgnore('.pyncignore')
    if realverbose:
        print(patterns)
    for f in os.listdir(src):   # every file and directory in the path 'src'
        ignore=False
        for pattern in patterns:
            if realverbose:
                print("regex pattern: "+pattern)
            pat = re.compile(pattern)
            if pat.match(f):
                if realverbose:
                    print("matches an ignore pattern")
                ignore=True

        pathname = os.path.join(src,f)  # combine 'src' and 'f' to create full path for current item
        pathname2 = os.path.join(dest,f)    # combine 'dest' and 'f' to create full path for current item
        if realverbose:
            print("Source: ",pathname)
        if not ignore:
            if os.path.isdir(pathname): # if the current item is a directory
                if realverbose:
                    print(pathname," is a directory")
                if not os.path.exists(pathname2):   # if the destination directory does not exist
                    if not quiet:
                        print("creating ",pathname2)
                    if realverbose:
                        print("recursing into "+pathname)
                    if not no_action:
                        os.makedirs(pathname2)  # create destination directory
                sync(pathname,pathname2,verbose,quiet,no_action)    # recursively sync data in directory
            elif os.path.isfile(pathname):  # if the current item is a file
                if realverbose:
                    print(pathname, " is a file")
                copyto(pathname,pathname2,verbose,quiet,no_action)  # copy to destination
            else:
                print('Error: skipping ' , pathname)   # else print error
        elif realverbose:
            print("Ignoring "+pathname)
    

def copyto(src,dest,verbose=False,quiet=False,no_action=False):
    if not os.path.exists(dest):
        if realverbose:
            print(dest, " does not exist, creating")
        if not no_action:
            shutil.copy2(src,dest)
        if not quiet:
            print(src, " -> ", dest)
    else:
        if realverbose:
            print(dest, " exists")
        if not filecmp.cmp(src,dest):
            if realverbose:
                print(src, " and ", dest, " are not identical")
            if os.path.getctime(src) > os.path.getctime(dest):
                if realverbose:
                    print(src, " is newer than ", dest)
                if not no_action:
                    shutil.copy2(src,dest)
                if not quiet:
                    print(src, " -> ", dest)
        elif realverbose:
            print(src, " and ", dest, " are identical")
    

# run the sync with the args
getIgnore(".pyncignore")
sync(args.source,args.dest,args.verbose,args.quiet,args.no_action)
