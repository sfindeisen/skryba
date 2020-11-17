import re
import unicodedata

from utils.log import debug

def normalize(s, allow_nonascii=True):
    """Applies Unicode normalization and optionally strips all non-ASCII characters."""
    if (allow_nonascii):
        return unicodedata.normalize('NFKC', s)
    else:
        return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')

def string2id(s, allow_nonascii=False, de_umlaut_aware=True):
    """
    Converts an arbitrary string to a friendly ID (eg. a file name). Unicode
    normalization is applied, whitespace and non-word characters are removed
    or substituted.
    """
    z = s

    # replace German umlauts with *e; replace scharfes s with ss
    if de_umlaut_aware:
        # scharfes s
        z = z.replace('\u1E9E', 'SS')
        z = z.replace('\u00DF', 'ss')

        # a umlaut
        z = z.replace('\u00C4', 'AE')
        z = z.replace('\u00E4', 'ae')

        # o umlaut
        z = z.replace('\u00D6', 'OE')
        z = z.replace('\u00F6', 'oe')

        # u umlaut
        z = z.replace('\u00DC', 'UE')
        z = z.replace('\u00FC', 'ue')

    z = normalize(z, allow_nonascii)
    z = re.sub(r'[^\w\s-]', '', z).strip()
    z = re.sub(r'[-\s]+', '-', z)
    debug("string2id: {} => {}".format(s,z))
    return z
