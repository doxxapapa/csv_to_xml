def update_values(main_dict, other_dict):
    """
    This will update the values of the initial dict. It runs through the dict, and parses the elements. 
    If the current element is a dict in the schema, it will update its value, recursively.
    """
    for key in main_dict:
        matching_key = next((keyd for keyd in other_dict if str(keyd).startswith(str(key))), None)
        if matching_key != None:
            if isinstance(main_dict[key], dict):
                update_values(main_dict[key], other_dict)
            elif matching_key.startswith(key):
                main_dict[key] = other_dict.get(matching_key, main_dict[key])
    return main_dict