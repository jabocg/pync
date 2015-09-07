#!/usr/bin/env python
import os, sys, shutil, filecmp
import argparse
from stat import *

parser = argparse.ArgumentParser()
parser.add_argument("source", help="directory to sync from")
parser.add_argument("dest", help="directory to sync to")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
args = parser.parse_args()


def sync(src,dest,verbose=False):
    for f in os.listdir(src):   # every file and directory in the path 'src'
        pathname = os.path.join(src,f)  # combine 'src' and 'f' to create full path for current item
        pathname2 = os.path.join(dest,f)    # combine 'dest' and 'f' to create full path for current item
        if verbose:
            print("Source: ",pathname)
        if os.path.isdir(pathname): # if the current item is a directory
            if verbose:
                print(pathname," is a directory")
            if not os.path.exists(pathname2):   # if the destination directory does not exist
                print("creating ",pathname2)
                if verbose:
                    print("recursing into ",pathname)
                os.makedirs(pathname2)  # create destination directory
            sync(pathname,pathname2,verbose)    # recursively sync data in directory
        elif os.path.isfile(pathname):  # if the current item is a file
            if verbose:
                print(pathname, " is a file")
            copyto(pathname,pathname2,verbose)  # copy to destination
        else:
            print('Error: skipping ' , pathname)   # else print error
    

def copyto(src,dest,verbose=False):
    if not os.path.exists(dest):
        if verbose:
            print(dest, " does not exist, creating")
        shutil.copy2(src,dest)
        print(src, " -> ", dest)
    else:
        if verbose:
            print(dest, " exists")
        if not filecmp.cmp(src,dest):
            if verbose:
                print(src, " and ", dest, " are not identical")
            if os.path.getctime(src) > os.path.getctime(dest):
                if verbose:
                    print(src, " is newer than ", dest)
                shutil.copy2(src,dest)
                print(src, " -> ", dest)
        elif verbose:
            print(src, " and ", dest, " are identical")
    

# run the sync with the args
sync(args.source,args.dest,args.verbose)
