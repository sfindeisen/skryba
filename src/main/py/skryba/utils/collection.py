def filter_dict(kv, p):
    """Given a dictionary, returns a new one retaining only pairs satisfying the predicate."""
    return { k:v for k,v in kv.items() if p(k,v) }

def filter_dict_values_not_none(kv):
    """Given a dictionary, returns a new one retaining only pairs where value is not None."""
    return filter_dict(kv, lambda k, v : (v is not None))
