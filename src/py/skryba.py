#!/usr/bin/python3

import abc

class Base(abc.ABC):
    """Abstract base class in Skryba chain."""
    def __init__(self, parent=None):
        self.parent = parent

import fileset
import utils.log
import utils.text

################################################################
# Export these functions to the top level
################################################################
verbose   = utils.log.set_verbose
info      = utils.log.info
debug     = utils.log.debug
string2id = utils.text.string2id
listdir   = fileset.listdir
