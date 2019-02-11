#!/usr/bin/python3

import re
import unicodedata

def normalize(s, allow_nonascii=True):
    """Applies Unicode normalization and optionally strips all non-ASCII characters."""
    if (allow_nonascii):
        return unicodedata.normalize('NFKC', s)
    else:
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')

def string2id(s, allow_nonascii=False):
    """
    Converts an arbitrary string to a friendly ID (eg. a file name). Unicode
    normalization is applied, whitespace and non-word characters are removed
    or substituted.
    """
    s = normalize(s, allow_nonascii)
    s = re.sub(r'[^\w\s-]', '', s).strip()
    s = re.sub(r'[-\s]+', '-', s)
    return s
