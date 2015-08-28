#!/usr/bin/env python
import os, sys, shutil, filecmp
from stat import *

PATH = "/home/jabocg/Documents/Test/"
SRC = "Source/"
DEST = "Dest/"


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
    # if debug:
    #     print "DEBUG:"
    #     print "    src ctime:  ",os.path.getctime(src)
    #     if os.path.exists(dest):
    #         print "    dest ctime: ",os.path.getctime(dest)
    #     else:
    #         print "    dest file does not exist"
    # if os.path.isfile(src) and os.path.isfile(dest):    # if both files exist, and are files
    #     if debug:
    #         print "DEBUG: both are files"
    #     if os.path.getctime(src) > os.path.getctime(dest):  # and the 'src' is newer
    #         if debug:
    #             print "DEBUG: "
    #             print "    src ctime:  ", os.path.getctime(src)
    #             print "    dest ctime: ", os.path.getctime(dest)
    #         print src, ' -> ', dest
    #         shutil.copy2(src,dest)  # copy source to destination
    # elif not os.path.exists(dest):  # if the destination file does not exist
    #     if debug:
    #         print "DEBUG: dest file does not exist"
    #     print src, ' -> ', dest
    #     # open(dest,'w+') # create the destination file
    #     shutil.copy2(src,dest)  # and copy the source file to it
    
#sync(PATH+SRC,PATH+DEST)

if len(sys.argv) < 3:
    print 'Please give two arguments: a source directory and a destination directory'
else:
    sync(sys.argv[1],sys.argv[2])
    #sync(sys.argv[1],sys.argv[2],True)


