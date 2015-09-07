#!/usr/bin/env python
import os, sys, shutil, filecmp
import argparse
from stat import *

parser = argparse.ArgumentParser()
parser.add_argument("source", help="directory to sync from")
parser.add_argument("dest", help="directory to sync to")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-q", "--quiet", help="suppress output, except errors, OVERRIDES --verbose", action="store_true")
parser.add_argument("-n", "--no-action", help="do NOT copy files, only print what would happen", action="store_true")
args = parser.parse_args()


def sync(src,dest,verbose=False,quiet=False,no_action=False):
    for f in os.listdir(src):   # every file and directory in the path 'src'
        pathname = os.path.join(src,f)  # combine 'src' and 'f' to create full path for current item
        pathname2 = os.path.join(dest,f)    # combine 'dest' and 'f' to create full path for current item
        if verbose and not quiet:
            print("Source: ",pathname)
        if os.path.isdir(pathname): # if the current item is a directory
            if verbose and not quiet:
                print(pathname," is a directory")
            if not os.path.exists(pathname2):   # if the destination directory does not exist
                if not quiet:
                    print("creating ",pathname2)
                if verbose and not quiet:
                    print("recursing into ",pathname)
                if not no_action:
                    os.makedirs(pathname2)  # create destination directory
            sync(pathname,pathname2,verbose,quiet,no_action)    # recursively sync data in directory
        elif os.path.isfile(pathname):  # if the current item is a file
            if verbose and not quiet:
                print(pathname, " is a file")
            copyto(pathname,pathname2,verbose,quiet,no_action)  # copy to destination
        else:
            print('Error: skipping ' , pathname)   # else print error
    

def copyto(src,dest,verbose=False,quiet=False,no_action=False):
    if not os.path.exists(dest):
        if verbose and not quiet:
            print(dest, " does not exist, creating")
        if not no_action:
            shutil.copy2(src,dest)
        if not quiet:
            print(src, " -> ", dest)
    else:
        if verbose and not quiet:
            print(dest, " exists")
        if not filecmp.cmp(src,dest):
            if verbose and not quiet:
                print(src, " and ", dest, " are not identical")
            if os.path.getctime(src) > os.path.getctime(dest):
                if verbose and not quiet:
                    print(src, " is newer than ", dest)
                if not no_action:
                    shutil.copy2(src,dest)
                if not quiet:
                    print(src, " -> ", dest)
        elif verbose and not quiet:
            print(src, " and ", dest, " are identical")
    

# run the sync with the args
sync(args.source,args.dest,args.verbose,args.quiet,args.no_action)
