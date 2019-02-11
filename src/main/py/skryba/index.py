#!/usr/bin/python3

import fileset
import utils.log
import utils.text

################################################################
# Export these functions to the top level
################################################################
verbose          = utils.log.set_verbose
info             = utils.log.info
debug            = utils.log.debug
normalize_string = utils.text.normalize
string2id        = utils.text.string2id
listdir          = fileset.listdir
