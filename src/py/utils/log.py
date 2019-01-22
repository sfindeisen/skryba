#!/usr/bin/python3

f_verbose = False

def set_verbose(verbose):
    global f_verbose
    f_verbose = bool(verbose)

def debug(msg):
    global f_verbose
    if (f_verbose):
        print(msg)

def info(msg):
    print (msg)
