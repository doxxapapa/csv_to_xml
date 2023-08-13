def add_values(main_dict, csv_input):
    """
    This will add values for the generated dict from csv
    """
    for key in main_dict:
        try:
            if isinstance(main_dict[key], dict):
               add_values(main_dict[key], csv_input)
            else:
               main_dict[key] = csv_input[key]
        except KeyError as e:
            continue
    return main_dict