
def modify_element(element):
    """
    This module will handle the modification of the elements. Add new logic if a schema is failing.
    """
    if element.endswith('.0'):
        return element[:-2]  # Remove the last two characters
    if element == "True" or element == "False":
        return element.lower()
    return element
