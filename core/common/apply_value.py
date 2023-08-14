def update_values(main_dict, other_dict):
    for key in main_dict:
        if isinstance(main_dict[key], dict):
            update_values(main_dict[key], other_dict)
        elif key in other_dict:
            main_dict[key] = other_dict[key]
    return main_dict