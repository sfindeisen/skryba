# Alphabet of digits, used for number conversions between different bases.
# Note: there is no "I".
digits = "0123456789ABCDEFGHJKLMNOPQRSTUVWXYZ"

def int2str(k, base=len(digits), min_length=0):
    """
    Integer to string in a given base. If min_length is specified, then the result
    will be prepended with zeroes if appropriate (not including the leading minus
    sign).
    """
    if (base < 2) or (len(digits) < base):
        raise ValueError("Base out of range ({})".format(base))
    if (0 == k):
        return digits[0]

    neg = (k < 0)
    k   = abs(k)
    res = []

    while (1 <= k):
        res.append(digits[k % base])
        k //= base
    while (len(res) < min_length):
        res.append(digits[0])
    if neg:
        res.append('-')
    res.reverse()
    return ''.join(res)
