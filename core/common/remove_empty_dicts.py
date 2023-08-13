def remove_empty_dicts(d, exceptions):
    """
    This will remove any empty dicts, except if the dict is in exceptions list.
    """
    return {
        k: remove_empty_dicts(v, exceptions) if isinstance(v, dict) else v
        for k, v in d.items() if (
            (k in exceptions) or
            (v != {} and (not isinstance(v, dict) or remove_empty_dicts(v, exceptions)))
        )
    }