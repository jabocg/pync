#!/usr/bin/env python
import os, sys, shutil, filecmp
from stat import *


def sync(src,dest,debug=False):

    for f in os.listdir(src):   # every file and directory in the path 'src'
        pathname = os.path.join(src,f)  # combine 'src' and 'f' to create full path for current item
        pathname2 = os.path.join(dest,f)    # combine 'dest' and 'f' to create full path for current item
        if debug:
            print "DEBUG:"
            print "    pathname:  ",pathname
            print "    pathname2: ",pathname2
        if os.path.isdir(pathname): # if the current item is a directory
            if debug:
                print "DEBUG: ",pathname, " is a directory"
            if not os.path.exists(pathname2):   # if the destination directory does not exist
                print pathname2, " does not exist, creating" 
                os.makedirs(pathname2)  # create destination directory
            sync(pathname,pathname2,debug)    # recursively sync data in directory
        elif os.path.isfile(pathname):  # if the current item is a file
            if debug:
                print "DEBUG: ", pathname, " is a file"
            copyto(pathname,pathname2,debug)  # copy to destination
        else:
            print 'Error: skipping ' , pathname   # else print error
    

def copyto(src,dest,debug=False):
    if not os.path.exists(dest):
        shutil.copy2(src,dest)
        print src, " -> ", dest
    else:
        if not filecmp.cmp(src,dest):
            if os.path.getctime(src) > os.path.getctime(dest):
                shutil.copy2(src,dest)
                print src, " -> ", dest
    

if len(sys.argv) < 3:
    print 'Please give two arguments: a source directory and a destination directory'
else:
    sync(sys.argv[1],sys.argv[2])
    #sync(sys.argv[1],sys.argv[2],True)


