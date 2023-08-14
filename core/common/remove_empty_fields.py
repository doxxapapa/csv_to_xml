def remove_empty_fields(d, exceptions):
    """
    This will remove any empty fields, except if the dict is in exceptions list.
    """
    return {k: remove_empty_fields(v, exceptions) if isinstance(v, dict) else v
            for k, v in d.items() if k in exceptions or v != ''}
