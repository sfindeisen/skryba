#!/usr/bin/python3

import os
import shutil

from utils.log import debug, info

# Overwrite all output files?
f_overwrite_all = False

def prompt_overwrite(dst):
    global f_overwrite_all

    while True:
        c = input("File exists: " + dst + " . Overwrite? [Yes/No/All/Quit]: ").lower()

        if ('y' == c):
            return True
        if ('n' == c):
            return False
        if ('a' == c):
            f_overwrite_all = True
            return True
        if ('q' == c):
            raise Exception("Quit")

def copyfile(src, dst):
    """Moves dst to src, prompting for overwrite if dst exists."""
    if os.path.exists(dst):
        if os.path.isdir(dst):
            raise Exception("Destination file exists and is a directory: " + dst + " . Delete it manually.")
        else:
            if (f_overwrite_all or prompt_overwrite(dst)):
                info("W " + dst)
                shutil.move(src, dst, copy_function=shutil.copy)
    else:
        info("W " + dst)
        shutil.move(src, dst)

def copytree(src, dst):
    """Recursively copies src into dst."""
    os.makedirs(name=dst, mode=0o700, exist_ok=True)

    for x in os.listdir(src):
        s = os.path.join(src, x)
        d = os.path.join(dst, x)
        if os.path.isdir(s):
            copytree(s, d)      # recursive call
        else:
            copyfile(s, d)

def write_file(filename, contents):
    """Writes contents into a file."""
    debug("W " + filename)
    with open(filename,'xb') as f:
        f.write(contents)
