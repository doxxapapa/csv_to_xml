from .modify_element import modify_element
from lxml import etree

def dict_to_xml(element, data):
    """
    This wil lconvert the dictionary into an xml.
    """
    for key, value in data.items():
        if isinstance(value, dict):
            sub_element = etree.SubElement(element, key)
            dict_to_xml(sub_element, value)
        else:
            etree.SubElement(element, key).text = modify_element(data[key])