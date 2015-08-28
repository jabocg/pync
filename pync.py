#!/usr/bin/env python
import os, sys, shutil
from stat import *

PATH = "/home/jabocg/Documents/Test/"
SRC = "Source/"
DEST = "Dest/"


def sync(src,dest,debug=0):

    for f in os.listdir(src):   # every file and directory in the path 'src'
        pathname = os.path.join(src,f)  # combine 'src' and 'f' to create full path for current item
        pathname2 = os.path.join(dest,f)    # combine 'dest' and 'f' to create full path for current item
        if os.path.isdir(pathname): # if the current item is a directory
            if not os.path.exists(pathname2):   # if the destination directory does not exist
                print "dest directory does not exist, creating" 
                os.makedirs(pathname2)  # create destination directory
            sync(pathname,pathname2)    # recursively sync data in directory
        elif os.path.isfile(pathname):  # if the current item is a file
            copyto(pathname,pathname2)  # copy to destination
        else:
            print 'Error: skipping %s' % pathname   # else print error
            
    

def copyto(src,dest,debug=0):
    print "src ctime:  ",os.path.getctime(src)
    print "dest ctime: ",os.path.getctime(dest)
    if os.path.isfile(src) and os.path.isfile(dest):    # if both files exist, and are files
        if os.path.getctime(src) > os.path.getctime(dest):  # and the 'src' is newer
            print 'copying from ', src, ' to ', dest
            shutil.copy2(src,dest)  # copy source to destination
    elif not os.path.exists(dest):  # if the destination file does not exist
        print 'copying from ', src, ' to ', dest
#        open(dest,'w+') # create the destination file
        shutil.copy2(src,dest)  # and copy the source file to it
    
#sync(PATH+SRC,PATH+DEST)

if len(sys.argv) < 3:
    print 'Please give two arguments: a source directory and a destination directory'
else:
    sync(sys.argv[1],sys.argv[2],1)


