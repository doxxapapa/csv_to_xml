from lxml import etree

def validate_xml(xml_filename, xsd_filename):
    try:
        xml_doc = etree.parse(xml_filename)
        xsd_doc = etree.parse(xsd_filename)
        xsd_schema = etree.XMLSchema(xsd_doc)
        
        is_valid = xsd_schema.validate(xml_doc)
        
        if is_valid:
            print("XML is valid according to the XSD schema.")
        else:
            print("XML is not valid according to the XSD schema.")
            print(xsd_schema.error_log)
            
    except etree.XMLSyntaxError as e:
        print("XML syntax error:", e)