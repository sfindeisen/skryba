#!/usr/bin/python3

import os
import shutil

from os import makedirs
from os.path import abspath, dirname, exists, isdir
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

def _copy(src, dst):
    """Copies src to dst."""
    info("W " + dst)
    shutil.copy(src, dst)

def _copyfile(src, dst):
    """Copies src to dst, prompting for overwrite if dst exists."""
    if os.path.exists(dst):
        if os.path.isdir(dst):
            raise Exception("Destination file exists and is a directory: " + dst + " . Delete it manually.")
        else:
            if (f_overwrite_all or prompt_overwrite(dst)):
                _copy(src, dst)
    else:
        _copy(src, dst)

def _copytree(src, dst, exclude=[]):
    """Recursively copies src to dst."""
    if (src in exclude):
        return

    os.makedirs(name=dst, mode=0o700, exist_ok=True)

    for x in os.listdir(src):
        s = os.path.join(src, x)
        d = os.path.join(dst, x)
        if os.path.isdir(s):
            _copytree(s, d, exclude=exclude)   # recursive call
        else:
            _copyfile(s, d)

def copytree(src, dst, exclude=[]):
    _copytree(abspath(src), abspath(dst), exclude=exclude)

def write_file(filename, contents, overwrite=False):
    """Writes contents into a file."""
    fabs = abspath(filename)
    debug("W " + fabs)

    if exists(fabs):
        if isdir(fabs):
            raise Exception("Destination file exists and is a directory: " + fabs + " . Delete it manually.")
        else:
            if (f_overwrite_all or overwrite or prompt_overwrite(fabs)):
                with open(fabs,'wb') as f:
                    f.write(contents)
    else:
        makedirs(dirname(fabs), mode=0o700, exist_ok=True)
        with open(fabs,'xb') as f:
            f.write(contents)
