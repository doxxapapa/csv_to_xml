import os
from lxml import etree
import csv
from zipfile import ZipFile

def apply_schema(schema_path, csv_path):
    
    # Load XSD schema
    xmlschema = etree.XMLSchema(file=schema_path)

    # Open CSV file and XML output file
    xml_output_file = "output.xml"

    # Create root XML element
    root = etree.Element("Students")
    
    xsd_file = schema_path
    xsd_tree = etree.parse(xsd_file)
    xsd_root = xsd_tree.getroot()
    
    group_elements = {}
    element_lsit = []
    element_xpath = ".//xs:sequence/xs:element | .//xs:attribute | .//xs:all/xs:element"
    root_path = "//xs:complexType | //xs:simpleType"
    first_element = {"birth_number": ''}
    diic = {}
    for complex_type in xsd_root.xpath(root_path, namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
        group_name = complex_type.get("name")
        ddd = {}
        if group_name != None:
            [ddd.update({element.get("name"): ""}) for element in complex_type.xpath(element_xpath, namespaces={"xs": "http://www.w3.org/2001/XMLSchema"})]
            temp_dict = {group_name: ddd}
            diic.update(temp_dict)
    # Traverse the XSD schema to identify complex types with sequences
    for complex_type in xsd_root.xpath("//xs:element[@name='Student']/xs:complexType/xs:sequence/xs:element", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}):
        group_name = complex_type.get("name")
        ty = complex_type.get("type")
        group_elements[group_name] = ""
        if str(ty).endswith("Type"):
            if not diic[ty]:
                diic[ty] = ""
            group_elements[group_name] = diic[ty]
    
    dd = update_values(group_elements, diic)
    del dd['Study']['Consultant']
    del dd['Study']['Payments']
    del dd['Study']['Mobility']
    del dd["SpecialNeeds"]
    final_dict = []
    with open(csv_path, "r", encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            template_dd = dd
            return_dd = add_values(template_dd, row)
            exceptions = ["BuildingNumber", "Faculty",]
            dict_exceptions = []
            return_dd = remove_empty_values_smarter(return_dd, exceptions)
            return_dd = remove_empty_dicts_smarter(return_dd, dict_exceptions)
            final_dict.append(add_values(return_dd, row))
    
    stundents = etree.Element('Students')
    
    # Create a string representation with indentation

    # Write the formatted XML to a file
    
    is_equal = False
    # Open and read CSV file
    with open(csv_path, "r",  encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for index, row in enumerate(csv_reader):
            altered_row = {key: process_element(value) for key, value in row.items()}
            student = etree.SubElement(stundents, 'Student')
            student.set('birth_number', altered_row['birth_number'])
            dict_to_xml(student, final_dict[index])
            
            # Validate the created XML element against the schema
            #if xmlschema.validate(xml_element):
            #    root.append(xml_element)
        xml_string = etree.tostring(stundents, encoding='utf-8', pretty_print=True, xml_declaration=True,)
        xml_string = xml_string.decode('utf-8')
        with open('outputs/output.xml', 'w', encoding='utf-8') as xml_file:
                xml_file.write(str(xml_string))
    create_zip()   
    validate_xml("outputs/output.xml", schema_path )
    #validate_x            
    #validate_xml(Path([os.getcwd(), "output.xml"], )
def update_values(main_dict, other_dict):
        for key in main_dict:
            matching_key = next((keyd for keyd in other_dict if str(keyd).startswith(str(key))), None)
            if matching_key != None:
                if isinstance(main_dict[key], dict):
                    update_values(main_dict[key], other_dict)
                elif matching_key.startswith(key):
                    main_dict[key] = other_dict.get(matching_key, main_dict[key])
        return main_dict


def add_values(main_dict, csv_input):
        for key in main_dict:
            try:
                
                if isinstance(main_dict[key], dict):
                    add_values(main_dict[key], csv_input)
                else:
                    main_dict[key] = csv_input[key]
            except KeyError as e:
                continue
        return main_dict

def dict_to_xml(element, data):
    for key, value in data.items():
        if isinstance(value, dict):
            sub_element = etree.SubElement(element, key)
            dict_to_xml(sub_element, value)
        else:
            etree.SubElement(element, key).text = process_element(data[key])
            
def remove_empty_values(d):
    return {k: remove_empty_values(v) if isinstance(v, dict) else v for k, v in d.items() if v != ''}

def remove_empty_values_smarter(d, exceptions):
    return {k: remove_empty_values_smarter(v, exceptions) if isinstance(v, dict) else v
            for k, v in d.items() if k in exceptions or v != ''}


# Function to recursively remove entries with empty dictionaries
def remove_empty_dicts(d):
    return {
        k: remove_empty_dicts(v) if isinstance(v, dict) else v
        for k, v in d.items() if (v != {} and (not isinstance(v, dict) or remove_empty_dicts(v)))
    }

def remove_empty_dicts_smarter(d, exceptions):
    return {
        k: remove_empty_dicts_smarter(v, exceptions) if isinstance(v, dict) else v
        for k, v in d.items() if (
            (k in exceptions) or
            (v != {} and (not isinstance(v, dict) or remove_empty_dicts_smarter(v, exceptions)))
        )
    }

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
        
def process_row(row):
    processed_row = []
    for element in row:
        if element.endswith('.0'):
            processed_row.append(element[:-2])  # Remove the last two characters
        else:
            processed_row.append(element)
    return processed_row

def process_element(element):
    if element.endswith('.0'):
        return element[:-2]  # Remove the last two characters
    if element == "True" or element == "False":
        return element.lower()
    return element

def create_zip():
    # Path to the XML file
    xml_file_path = 'outputs/output.xml'
    
    # Path to the zip archive
    zip_file_path = 'output.zip'

    # Create a zip archive
    with ZipFile(f"outputs/{zip_file_path}", 'w') as zip_file:
        # Add the XML file to the archive
        zip_file.write(xml_file_path, arcname='output.xml')