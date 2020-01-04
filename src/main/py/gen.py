#!/usr/bin/python3

import argparse

from skryba.index import verbose, force_overwrite, warning, info, debug, parse, read_file, Environment

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='gen.py',
        add_help=True, allow_abbrev=False, epilog="""This program comes with ABSOLUTELY NO WARRANTY.""")

    parser.add_argument("--verbose", required=False, action="store_true", help="Verbose processing")
    parser.add_argument("--overwrite-all", required=False, action="store_true", help="Overwrite all files without prompting (batch mode)")
    parser.add_argument("--ctrl", required=True, metavar="FILE", help="Skryba control program")
    parser.add_argument(metavar="output-dir", dest="outdir", help="Output directory")
    args = parser.parse_args()

    if (args.verbose):
        verbose(True)
    if (args.overwrite_all):
        force_overwrite()

    skryba_program = read_file(args.ctrl)
    debug("Skryba program ({}): {}".format(args.ctrl, skryba_program))
    parse_tree = parse(skryba_program)
    debug("parse_tree type: {}".format(type(parse_tree)))
    debug("parse_tree: {}".format(parse_tree))

    if (parse_tree is not None):
        parse_tree.compile(Environment())
